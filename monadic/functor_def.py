from monadic.function import compose, identity


def functor_law_identity(F, a):
    lhs = F(identity)(a)
    rhs = a
    if lhs != rhs:
        raise Exception("Functor identity law is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


def functor_law_compose(F, f, g, a):
    lhs = compose(F(f), F(g))(a)
    rhs = F(compose(f, g))(a)
    if lhs != rhs:
        raise Exception("Functor composite law is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


# Test functions


def add1(x):
    return (x + 1)


def add2(x):
    return (x + 2)
