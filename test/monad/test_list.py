from monadic.decorator import monadic
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.list import list_monad

from nose.tools import eq_


test_data = [
    [[[]]],
    [[[1]]],
    [[[1,2],[1]],[[1],[2,3]]]
]


test_monad = list_monad()


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, test_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, test_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, test_monad, xs


@monadic(list_monad)
def decorated_list():
    x = range(0, 4)
    y = range(0, x)
    return y


def test_decorated_list():
    xs = decorated_list()
    expected = [0, 0, 1, 0, 1, 2]
    eq_(expected, xs, "List non calculated correctly")
