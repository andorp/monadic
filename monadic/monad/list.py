from monadic.monad_def import monad
from monadic.interop import map_list


def list_functor(c):
    def fmap(l):
        return map_list(c, l)
    return fmap


def unit(x):
    return [x]


def join(xss):
    result = []
    for xs in xss:
        result = result + xs
    return result


def list_monad():
    return monad(list_functor, join, unit)
