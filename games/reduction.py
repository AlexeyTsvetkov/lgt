from terms import *
from exceptions import *

def check_if_nat(term, message="Nat expected"):
    if not isinstance(term, Nat):
        raise GameException(message)

def get_slot(queryset, slot_id):
    try:
        return queryset.filter(slot_id=slot_id)[0]
    except:
        raise GameException("slot " + str(slot_id) + "not found")

def get_my_slot(request, slot_id):
    return get_slot(request.my_slots, slot_id)

def handle_ready_builtin(fn, request):
    fn.applied_args = map(lambda x: make_reduction(x, request), fn.applied_args)

    if isinstance(fn, Succ):
        check_if_nat(fn.applied_args[0])
        return Nat(value=fn.applied_args[0].value + 1)

    if isinstance(fn, Dbl):
        check_if_nat(fn.applied_args[0])
        return Nat(value=fn.applied_args[0].value * 2)

    if isinstance(fn, Get):
        check_if_nat(fn.applied_args[0])
        slot_id = fn.applied_args[0].value

        slot = get_my_slot(request, slot_id)

        return slot.term

    if isinstance(fn, Inc):
        check_if_nat(fn.applied_args[0])
        slot_id = fn.applied_args[0].value

        slot = get_my_slot(request, slot_id)

        slot.value += 1
        slot.save()

        return create_identity()

    if isinstance(fn, Dec):
        check_if_nat(fn.applied_args[0])
        slot_id = fn.applied_args[0].value

        slot = get_slot(request.opponent_slots, slot_id)

        slot.value -= 1
        slot.save()

        return create_identity()

    if isinstance(fn, Copy):
        check_if_nat(fn.applied_args[0])
        slot_id = fn.applied_args[0].value

        slot = get_slot(request.opponent_slots, slot_id)

        return slot.term

    raise GameException("Unknown builtin type: " + str(fn.__class__))

#########################

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

def make_reduction(term, request):
    if isinstance(term, Application):
        term.first_term = make_reduction(term.first_term, request)
        first = term.first_term

        second = term.second_term

        if isinstance(first, Nat) and isinstance(second, Nat):
            return Nat(value=first.value ** second.value)

        if isinstance(first, Abstraction):
            return make_reduction(replace_var(first.var_name, first.body, second), request)

        if isinstance(first, BuiltinFunction):

            first.apply_to(second)

            if first.is_ready():
                return handle_ready_builtin(first, request)

        raise GameException(str(first) + " is not applicable")

    return term
