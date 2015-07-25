from monadic.decorator import monadic, monadic_comp
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.list import list_monad
from monadic.monad_test import MonadLawTest

from nose.tools import eq_


__ALL__ = ['test_decorated_list',
           'test_list_comprehension',
           'ListMonadTest']

test_data = [
    [[[]]],
    [[[1]]],
    [[[1, 2], [1]], [[1], [2, 3]]]
]


class ListMonadTest(MonadLawTest):
    MONAD = list_monad()
    MONAD_TEST_DATA = test_data
    FUNCTOR_TEST_DATA = [[], [1]]


@monadic(list_monad)
def decorated_list():
    x = range(0, 4)
    y = range(0, x)
    return y


def test_decorated_list():
    xs = decorated_list()
    expected = [0, 0, 1, 0, 1, 2]
    eq_(expected, xs, "List non calculated correctly")


@monadic_comp(list_monad)
def comprehension_list():
    x = [y
         for x in range(0, 4)
         for y in range(0, x)]
    return x


def test_list_comprehension():
    xs = comprehension_list()
    expected = [0, 0, 1, 0, 1, 2]
    eq_(expected, xs, "List non calculated correctly")
