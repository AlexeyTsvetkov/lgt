from terms import *
from exceptions import *


class LimitCalls(object):
    def __init__(self, limit):
        self.limit = limit

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            if self.limit == 0:
                raise GameException("Reduction limit")

            self.limit -= 1

            return fn(*args, **kwargs)

        return wrapper


class Reducer(object):
    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_slot(queryset, slot_id):
        try:
            return queryset.filter(slot_id=slot_id)[0]
        except:
            raise GameException("Slot " + str(slot_id) + " not found")

    def get_my_slot(self, slot_id):
        return self.get_slot(self.request.my_slots, slot_id)

    def get_opponent_slot(self, slot_id):
        return self.get_slot(self.request.opponent_slots, slot_id)

    @staticmethod
    def check_if_nat(*terms):
        for term in terms:
            if not isinstance(term, Nat):
                raise GameException("Nat expected")

    @staticmethod
    def replace_var(var_name, term, arg):
        if isinstance(term, Variable):
            if term.name == var_name:
                return arg
            else:
                return term

        if isinstance(term, Application):
            return Application(
                first_term=Reducer.replace_var(var_name, term.first_term, arg),
                second_term=Reducer.replace_var(var_name, term.second_term, arg),
            )

        if isinstance(term, Abstraction):
            if term.var_name == var_name:
                return term

            new_var_name = term.var_name

            while new_var_name in arg.free_variables():
                new_var_name += '\''

            term.body = Reducer.replace_var(
                term.var_name,
                term.body,
                Variable(name=new_var_name)
            )

            term.var_name = new_var_name

            return Abstraction(
                var_name=term.var_name,
                body=Reducer.replace_var(
                    var_name,
                    term.body,
                    arg
                )
            )

        return term

    @LimitCalls(50)
    def make_reduction(self, term):
        if isinstance(term, Application):
            term.first_term = self.make_reduction(term.first_term)
            first = term.first_term

            second = term.second_term

            if isinstance(first, Nat) and isinstance(second, Nat):
                return Nat(value=first.value ** second.value)

            if isinstance(first, Abstraction):
                return self.make_reduction(self.replace_var(first.var_name, first.body, second))

            if isinstance(first, BuiltinFunction):

                first.apply_to(second)

                if first.is_ready():
                    return self.handle_ready_builtin(first)

                return first

            raise GameException(str(first) + " is not applicable")

        return term

    @LimitCalls(50)
    def handle_ready_builtin(self, fn):
        fn.applied_args = map(lambda x: self.make_reduction(x), fn.applied_args)

        if isinstance(fn, Succ):
            self.check_if_nat(fn.applied_args[0])
            return Nat(value=fn.applied_args[0].value + 1)

        if isinstance(fn, Dbl):
            self.check_if_nat(fn.applied_args[0])
            return Nat(value=fn.applied_args[0].value * 2)

        if isinstance(fn, Get):
            self.check_if_nat(fn.applied_args[0])
            slot_id = fn.applied_args[0].value

            slot = self.get_my_slot(slot_id)

            return slot.term

        if isinstance(fn, Inc):
            self.check_if_nat(fn.applied_args[0])
            slot_id = fn.applied_args[0].value

            slot = self.get_my_slot(slot_id)

            slot.value += 1
            slot.save()

            return create_identity()

        if isinstance(fn, Dec):
            self.check_if_nat(fn.applied_args[0])
            slot_id = fn.applied_args[0].value

            slot = self.get_slot(self.request.opponent_slots, slot_id)

            slot.value -= 1
            slot.save()

            return create_identity()

        if isinstance(fn, Copy):
            self.check_if_nat(fn.applied_args[0])
            slot_id = fn.applied_args[0].value

            slot = self.get_opponent_slot(slot_id)

            return slot.term

        if isinstance(fn, Attack):
            self.check_if_nat(*fn.applied_args)

            prop_slot_id = fn.applied_args[0].value
            opp_slot_id = fn.applied_args[1].value
            n = fn.applied_args[2].value

            prop_slot = self.get_my_slot(prop_slot_id)
            opp_slot = self.get_opponent_slot(opp_slot_id)

            prop_slot.value -= n
            opp_slot.value -= 2 * n

            prop_slot.save()
            opp_slot.save()

            return create_identity()

        raise GameException("Unknown builtin type: " + str(fn.__class__))


