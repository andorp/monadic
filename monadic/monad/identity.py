from monadic.function import identity
from monadic.monad_def import monad


def identity_functor(f):
    def fmap(x):
        return f(x)
    return fmap


def identity_monad():
    return monad(identity_functor, identity, identity)
