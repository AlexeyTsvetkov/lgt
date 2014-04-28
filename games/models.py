from mongoengine import *

connect('lgt')


class Term(EmbeddedDocument):
    meta = {'allow_inheritance': True}

    def bounded_variables(self):
        return set()

    def free_variables(self):
        return set()

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


class Nat(Term):
    value = IntField(0)

    def __str__(self):
        return str(self.value)


class Succ(Term):
    def __str__(self):
        return "succ"

class Dbl(Term):
    def __str__(self):
        return "dbl"


class Application(Term):
    first_term = EmbeddedDocumentField(Term)
    second_term = EmbeddedDocumentField(Term)

    def __str__(self):
        return str(self.first_term) + " " + str(self.second_term)

    def bounded_variables(self):
        return self.first_term.bounded_variables().union(self.second_term.bounded_variables())

    def free_variables(self):
        return self.first_term.free_variables().union(self.second_term.free_variables())


#########################

class Slot(Document):
    value = IntField()
    term = EmbeddedDocumentField(Term)

    def as_dict(self):
        return {
            'id': str(self.id),
            'value': self.value,
            'term': str(self.term)
        }


def create_identity():
    return Abstraction(var_name='x', body=Variable(name='x'))

def create_zero():
    result = Nat()
    result.value = 0
    return result
