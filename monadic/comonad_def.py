

def comonad(functor, cotimes, coident):
    return {
        'F': functor,
        '*': cotimes,  # F(a) -> F(F(a))
        '1': coident   # F(a) -> a
    }


def counit(comonad):
    def u(x):
        return (comonad['1'])(x)
    return u


def cokleisli_arrow(comonad):
    def fm(c, k):  # c: F(a) k: F(a) -> b
        F = comonad['F']
        return F(k)(comonad['*'](c))
    return fm


def comonad_law_one(comonad, a):
    F = comonad['F']
    delta = comonad['*']
    lhs = delta(delta(a))
    rhs = F(delta)(delta(a))
    if lhs != rhs:
        raise Exception("Comonad law one is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


def comonad_law_two(monad, a):
    delta = comonad['*']
    eps = comonad['1']
    lhs = eps(delta(a))
    rhs = a
    if lhs != rhs:
        raise Exception("Coonad law two is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


def monad_law_three(monad, a):
    F = comonad['F']
    delta = comonad['*']
    eps = comonad['1']
    lhs = G(eps)(delta(a))
    rhs = a
    if lhs != rhs:
        raise Exception("Comonad law 3 is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))
