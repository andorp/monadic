

def monad(functor, times, ident):
    return {
        'F': functor,
        '*': times,  # F(F(a)) -> F(a)
        '1': ident   # a       -> F(a)
    }


def kliesli_arrow(monad):
    def fm(m, k):
        F = monad['F']
        return monad['*'](F(k)(m))
    return fm


def unit(monad):
    def u(x):
        return (monad['1'])(x)
    return u


def monad_law_one(monad, a):
    F = monad['F']
    mu = monad['*']
    eta = monad['1']
    lhs = mu(F(mu)(a))
    rhs = mu(mu(a))
    if lhs != rhs:
        raise Exception("Monad law one is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


def monad_law_two(monad, a):
    mu = monad['*']
    eta = monad['1']
    lhs = mu(eta(a))
    rhs = a
    if lhs != rhs:
        raise Exception("Monad law two is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


def monad_law_three(monad, a):
    F = monad['F']
    mu = monad['*']
    eta = monad['1']
    lhs = mu(F(eta)(a))
    rhs = a
    if lhs != rhs:
        raise Exception("Monad law 3 is broken {lhs} = {rhs}".format(
            lhs=lhs, rhs=rhs))


class Monad(object):
    def __init__(self, monad_t, value):
        self.bind = kliesli_arrow(monad_t)
        self.value = value

    def __call__(self, k):
        self.value = self.bind(self.value, k)
        return self.value
