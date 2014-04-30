# -*- coding: utf-8 -*-
from terms import *


def is_simple_term(term):
    return isinstance(term, Variable) or isinstance(term, Nat)

def parents_if_not_simple(term):
    result = pretty_print(term)
    if not is_simple_term(term):
        result = "(%s)" % result

    return result

def pretty_print(term):
    if isinstance(term, Abstraction):
        body = term.body
        if isinstance(body, Abstraction):
            return u"λ %s%s" % (term.var_name, pretty_print(body)[1:])

        return u"λ %s.%s" % (term.var_name, pretty_print(body))

    if isinstance(term, Application):
        first = term.first_term
        first_repr = pretty_print(first)

        if isinstance(first, Abstraction):
            first_repr = "(" + first_repr + ")"

        second = term.second_term
        second_repr = parents_if_not_simple(second)

        return first_repr + " " + second_repr

    if isinstance(term, BuiltinFunction):
        part2 = " ".join(map(parents_if_not_simple, term.applied_args))
        part3 = " ".join(map(pretty_print, term.await_args_left))
        part1 = term.name

        return " ".join(filter(lambda x: len(x) > 0, (part1, part2, part3,)))

    return str(term)
