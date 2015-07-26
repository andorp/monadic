from monadic.decorator import monadic, monadic_comp
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.maybe import maybe_monad, nothing, just

from nose.tools import eq_


test_data = [
    nothing,
    just(nothing),
    just(just(nothing)),
    just(just(just(4))),
]


test_monad = maybe_monad()


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, test_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, test_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, test_monad, xs


def div_maybe(x, y):
    if y == 0:
        return nothing
    else:
        return just(x / y)


@monadic(maybe_monad)
def decorated_maybe():
    x = div_maybe(4, 2)
    y = div_maybe(4, x)
    return y


def test_decorated_maybe():
    xs = decorated_maybe()
    expected = just(2)
    eq_(expected, xs, "Maybe value is not calculated correctly")


@monadic_comp(maybe_monad)
def comprehension_maybe():
    x = [y
         for x in div_maybe(4, 2)
         for y in div_maybe(4, x)]
    return x


def test_maybe_comprehension():
    xs = comprehension_maybe()
    expected = just(2)
    eq_(expected, xs, "Maybe value is not calculated correctly")
