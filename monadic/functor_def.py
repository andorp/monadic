from monadic.function import compose


def functor_law_identity(F, a):
    lhs = F(id)(a)
    rhs = a
    if lhs != rhs:
        return Exception("Functor identity law is broken {lhs} = {rhs}".format(lhs=lhs, rhs=rhs))


def functor_law_compose(F, f, g, a):
    lhs = compose(F(f),F(g))(a)
    rhs = F(compose(f,g))(a)
    if lhs != rhs:
        raise Exception("Functor composite law is broken {lhs} = {rhs}".format(lhs=lhs, rhs=rhs))
