from monadic.decorator import monadic, monadic_comp
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.error import error_monad, Left, Right, error_msg
from monadic.monad_test import MonadLawTest

from nose.tools import eq_


__ALL__ = ['test_decorated_error',
           'test_comprehension',
           '']


test_data = [
    Left("error"),
    Right(Right(Right(3))),
    Right(Left("error"))
]


class MaybeMonadTest(MonadLawTest):
    MONAD = error_monad()
    MONAD_TEST_DATA = test_data
    FUNCTOR_TEST_DATA = [Left("error"), Right(3)]


def div_error(x, y):
    if y == 0:
        return error_msg("Divisor was zero")
    else:
        return Right(x / y)


@monadic(error_monad)
def decorated_error():
    x = 4
    y = div_error(16, x)
    z = div_error(y, 1)
    return z


def test_decorated_error():
    xs = decorated_error()
    expected = Right(4)
    eq_(expected, xs, "Right value is not calculated correctly")


@monadic_comp(error_monad)
def comprehension_error():
    x = [z
         for y in div_error(16, 4)
         for z in div_error(y, 1)]
    return x


def test_comprehension():
    xs = comprehension_error()
    expected = Right(4)
    eq_(expected, xs, "Right value is  not calculated correctly")
