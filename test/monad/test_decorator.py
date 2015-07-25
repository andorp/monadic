from monadic.decorator import monadic, monadic_comp
from monadic.monad.identity import identity_monad

from nose.tools import eq_


def div(x, y):
    return (x / y)


@monadic(identity_monad)
def decorated():
    x = div(4, 2)
    y = div(4, x)
    return y


def test_decorated():
    xs = decorated()
    expected = 2
    eq_(expected, xs, "Value is not calculated correctly")


@monadic_comp(identity_monad)
def comprehension():
    x = [z
         for y in div(16, 4)
         for z in div(y, 1)]
    return x


def test_comprehension():
    xs = comprehension()
    expected = 4
    eq_(expected, xs, "Right value is  not calculated correctly")
