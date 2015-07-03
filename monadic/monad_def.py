

def monad(functor, times, ident):
    return {
        't': functor,
        '*': times,
        '1': ident
    }


def flat_map(monad):
    def fm(m, k):
        F = monad['t']
        return monad['*'](F(k)(m))
    return fm


def monad_law_one(monad, a):
    F = monad['t']
    mu = monad['*']
    eta = monad['1']
    lhs = mu(F(mu)(a))
    rhs = mu(mu(a))
    if lhs != rhs:
       raise Exception("Monad law one is broken {lhs} = {rhs}".format(lhs=lhs, rhs=rhs))


def monad_law_two(monad, a):
    mu = monad['*']
    eta = monad['1']
    lhs = mu(eta(a))
    rhs = a
    if mu(eta(a)) != a:
        raise Exception("Monad law two is broken {lhs} = {rhs}".format(lhs=lhs, rhs=rhs))


def monad_law_three(monad, a):
    F = monad['t']
    mu = monad['*']
    eta = monad['1']
    lhs = mu(F(eta)(a))
    rhs = a
    if lhs != rhs:
        raise Exception("Monad law 3 is broken {lhs} = {rhs}".format(lhs=lhs, rhs=rhs))


