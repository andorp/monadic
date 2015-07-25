from monadic.functor_def import functor_law_identity, functor_law_compose
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three

from unittest import TestCase


__ALL__ = ['MonadLawTest']


def add1(x):
    return x + 1


def add2(x):
    return x + 2


class MonadLawTest(TestCase):
    MONAD = None
    MONAD_TEST_DATA = None

    FUNCTOR_TEST_DATA = None
    FUNCTOR_F1 = add1
    FUNCTOR_F2 = add2

    def test_functor_law_identity(self):
        FUNCTOR = MONAD['t']
        for xs in FUNCTOR_TEST_DATA:
            yield functor_law_identity, FUNCTOR, xs

    def test_functor_law_compose(self):
        FUNCTOR = MONAD['t']
        for xs in FUNCTOR_TEST_DATA:
            yield (functor_law_compose,
                   FUNCTOR,
                   FUNCTOR_F1,
                   FUNCTOR_F2,
                   xs)

    def test_monad_law_one(self):
        for xs in MONAD_TEST_DATA:
            yield monad_law_one, MONAD, xs

    def test_monad_law_two(self):
        for xs in MONAD_TEST_DATA:
            yield monad_law_two, MONAD, xs

    def test_monad_law_three(self):
        for xs in MONAD_TEST_DATA:
            yield monad_law_three, MONAD, xs
