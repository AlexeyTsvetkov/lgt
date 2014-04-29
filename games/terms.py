from mongoengine import *


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

class Copy(BuiltinFunction):
    def get_name(self):
        return "copy"

    def get_await_args(self):
        return "i",

class Attack(BuiltinFunction):
    def get_name(self):
        return "attack"

    def get_await_args(self):
        return "i", "j", "n"

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

def create_k_comb():
    return Abstraction(
        var_name='x',
        body=Abstraction(
            var_name='y',
            body=Variable(name='x')
        )
    )

#############################
