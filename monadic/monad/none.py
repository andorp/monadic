from monadic.monad_def import monad


__all__ = ['none_monad']


def none_functor(f):
    def fmap(x):
        if x is None:
            return x
        else:
            return f(x)
    return fmap


def unit(x):
    return x


def join(x):
    return x


def none_monad():
    return monad(none_functor, join, unit)
