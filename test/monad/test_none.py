from monadic.decorator import monadic, monadic_comp
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.none import none_monad


from nose.tools import eq_


test_data = [
    None,
    1,
    "String"
]


test_monad = none_monad()


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, test_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, test_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, test_monad, xs


def div_none(x, y):
    if y == 0:
        return None
    else:
        return (x / y)


@monadic(none_monad)
def decorated_none():
    x = div_none(4, 0)
    y = div_none(4, x)
    return y


def test_decorated():
    found = decorated_none()
    expected = None
    eq_(expected, found, "None guard does not work")


@monadic_comp(none_monad)
def comprehension_none():
    x = [ y for x in div_none(4, 0)
            for y in div_none(4, x)
        ]
    return x


def test_none_comprehension():
    xs = comprehension_none()
    expected = None
    eq_(expected, xs, "None is not calculated correctly")
