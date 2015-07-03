from monadic.monad_def import monad


def list_functor(c):
    def fmap(l):
        return map(c, l)
    return fmap


def unit(x):
    return [x]


def join(xss):
    result = []
    for xs in xss:
        result = result + xs
    return result


list_monad = monad(list_functor, join, unit)

