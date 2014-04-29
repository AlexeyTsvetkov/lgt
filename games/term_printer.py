from terms import *

def is_simple_term(term):
    return isinstance(term, Variable) or isinstance(term, Nat)

def pretty_print(term):
    if isinstance(term, Abstraction):
        body = term.body
        if isinstance(body, Abstraction):
            return "\%s %s" % (term.var_name, pretty_print(body)[1:])

        return "\%s -> %s" % (term.var_name, pretty_print(body))

    if isinstance(term, Application):
        first = term.first_term
        first_repr = pretty_print(first)

        if isinstance(first, Abstraction):
            first_repr = "(" + first_repr + ")"

        second = term.second_term
        second_repr = pretty_print(second)
        if not is_simple_term(second):
            second_repr = "(" + second_repr + ")"

        return first_repr + " " + second_repr
    return str(term)