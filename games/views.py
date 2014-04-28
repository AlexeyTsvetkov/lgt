from annoying.decorators import render_to, ajax_request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from models import *

@ajax_request
def create_slots(request):

    for slot in Slot.objects:
        slot.delete()

    for i in range(10):
        slot = Slot()
        slot.value = 100
        slot.term = create_identity()
        slot.save()

    return {'result': '1'}

@ajax_request
def slots(request):

    result = [slot.as_dict() for slot in Slot.objects]

    return {'slots': result}

KINDS = {
    'id': create_identity,
    'zero': create_zero,
    'succ': Succ
}

def replace_var(var_name, term, arg):
    if isinstance(term, Variable):
        if term.name == var_name:
            return arg
        else:
            return term

    if isinstance(term, Application):
        return Application(
            first_term=replace_var(var_name, term.first_term, arg),
            second_term=replace_var(var_name, term.second_term, arg),
        )

    if isinstance(term, Abstraction):
        if term.var_name == var_name:
            return term

        new_var_name = term.var_name

        while new_var_name in arg.free_variables():
            new_var_name += '\''

        term.body = replace_var(
                term.var_name,
                term.body,
                Variable(name=new_var_name)
            )

        term.var_name = new_var_name

        return Abstraction(
            var_name=term.var_name,
            body=replace_var(
                var_name,
                term.body,
                arg
            )
        )

    return term

class ReductionException(Exception):
    pass


def make_reduction(term):
    if isinstance(term, Application):
        term.first_term = make_reduction(term.first_term)
        first = term.first_term
        second = term.second_term

        if isinstance(first, Abstraction):
            return make_reduction(replace_var(first.var_name, first.body, second))

        if isinstance(first, Succ):
            if not isinstance(second, Nat):
                raise ReductionException("nat expected")

            return Nat(value=second.value + 1)

        if isinstance(first, Dbl):
            if not isinstance(second, Nat):
                raise ReductionException("nat expected")

            return Nat(value=second.value * 2)

        raise ReductionException(str(first) + " is not applicable")

    return term

#term = Application(
#    first_term=Abstraction(var_name='y', body=Abstraction(var_name='x', body=Variable(name='y'))),
#    second_term=Variable(name='x')
#)

@ajax_request
def apply_slot(request, id, kind, from_right):

    slot = Slot.objects(id=id)[0]

    term = KINDS[kind]()

    if int(from_right) == 1:
        application = Application(first_term=slot.term, second_term=term)
    else:
        application = Application(second_term=slot.term, first_term=term)
    try:
        new_slot_term = make_reduction(application)
    except ReductionException as e:
        return { 'error' : str(e) }

    slot.term = new_slot_term

    slot.save()

    return { 'slot' : slot.as_dict() }