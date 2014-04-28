from mongoengine import *

connect('lgt')


class Term(EmbeddedDocument):
    meta = {'allow_inheritance': True}

    def bounded_variables(self):
        return set()

    def free_variables(self):
        return set()

    def is_applicable(self):
        return False


class BuiltinFunction(Term):
    meta = {'allow_inheritance': True}

    applied_args = ListField(EmbeddedDocumentField(Term))

    def __str__(self):
        part2 = " ".join(map(str, self.applied_args))
        part3 = " ".join(map(str, self.await_args_left))
        part1 = self.name

        return " ".join((part1, part2, part3,))

    @property
    def name(self):
        return self.get_name()

    @property
    def await_args_left(self):
        return self.get_await_args()[len(self.applied_args):]

    def is_ready(self):
        return len(self.await_args_left) == 0

    def is_applicable(self):
        return not self.is_ready()

    def apply_to(self, arg):
        self.applied_args.append(arg)


class Variable(Term):
    name = StringField()

    def free_variables(self):
        return {self.name}

    def __str__(self):
        return self.name


class Abstraction(Term):
    var_name = StringField()
    body = EmbeddedDocumentField(Term)

    def __str__(self):
        return "\\" + self.var_name + " -> " + str(self.body)

    def free_variables(self):
        return self.body.free_variables() - {self.var_name}

    def bounded_variables(self):
        return self.body.bounded_variables().union({self.var_name})

    def is_applicable(self):
        return True


class Nat(Term):
    value = IntField(0)

    def __str__(self):
        return str(self.value)


class Succ(BuiltinFunction):
    def get_name(self):
        return "succ"

    def get_await_args(self):
        return "i",


class Dbl(BuiltinFunction):
    def get_name(self):
        return "dbl"

    def get_await_args(self):
        return "i",


class Get(BuiltinFunction):
    def get_name(self):
        return "get"

    def get_await_args(self):
        return "i",


class Inc(BuiltinFunction):
    def get_name(self):
        return "inc"

    def get_await_args(self):
        return "i",

class Dec(BuiltinFunction):
    def get_name(self):
        return "dec"

    def get_await_args(self):
        return "i",

class Application(Term):
    first_term = EmbeddedDocumentField(Term)
    second_term = EmbeddedDocumentField(Term)

    def __str__(self):
        return "(" + str(self.first_term) + ") (" + str(self.second_term) + ")"

    def bounded_variables(self):
        return self.first_term.bounded_variables().union(self.second_term.bounded_variables())

    def free_variables(self):
        return self.first_term.free_variables().union(self.second_term.free_variables())


#########################
class ReductionException(Exception):
    pass

def check_if_nat(term, message="Nat expected"):
    if not isinstance(term, Nat):
        raise ReductionException(message)

def get_slot(queryset, slot_id):
    try:
        return queryset.filter(slot_id=slot_id)[0]
    except:
        raise ReductionException("slot " + str(slot_id) + "not found")

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

    raise ReductionException("Unknown builtin type: " + str(fn.__class__))

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

        if not first.is_applicable():
            raise ReductionException(str(first) + " is not applicable")

        second = term.second_term

        if isinstance(first, Abstraction):
            return make_reduction(replace_var(first.var_name, first.body, second), request)

        if isinstance(first, BuiltinFunction):

            first.apply_to(second)

            if first.is_ready():
                return handle_ready_builtin(first, request)

    return term


#########################


def create_identity():
    return Abstraction(var_name='x', body=Variable(name='x'))

def create_zero():
    result = Nat()
    result.value = 0
    return result

def create_s_comb():
    return Abstraction(
        var_name='f',
        body=Abstraction(
            var_name='g',
            body=Abstraction(
                var_name='x',
                body=Application(
                    first_term=Application(
                        first_term=Variable(name='f'),
                        second_term=Variable(name='x'),
                    ),
                    second_term=Application(
                        first_term=Variable(name='g'),
                        second_term=Variable(name='x')
                    )
                )
            )
        )
    )

#############################

class Slot(Document):
    slot_id = IntField()

    game_id = ObjectIdField()
    user_id = IntField()

    value = IntField()
    term = EmbeddedDocumentField(Term)

    def as_dict(self):
        return {
            'id': str(self.slot_id),
            'value': self.value,
            'term': str(self.term)
        }

class Game(Document):
    first_user_id = IntField()
    second_user_id = IntField()

    first_slots = ListField(ReferenceField(Slot))
    second_slots = ListField(ReferenceField(Slot))

    def accept_opponent(self, opponent_id):
        self.second_user_id = opponent_id

        def add_slots(lst, user_id):
            for i in range(10):
                slot = Slot()
                slot.slot_id = i+1
                slot.game_id = self.id
                slot.user_id = user_id
                slot.value = 100
                slot.term = create_identity()
                slot.save()
                lst.append(slot)

        add_slots(self.first_slots, self.first_user_id)
        add_slots(self.second_slots, self.second_user_id)

        self.save()


