from monadic.decorator import monadic, monadic_comp
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.error import error_monad, Left, Right, error_msg


from nose.tools import eq_


test_data = [
    Left("error"),
    Right(Right(Right(3))),
    Right(Left("error"))
]


test_monad = error_monad()


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, test_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, test_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, test_monad, xs


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
