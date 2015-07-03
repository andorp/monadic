from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.list import list_monad


test_data = [
    [[[]]],
    [[[1]]],
    [[[1,2],[1]],[[1],[2,3]]]
]


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, list_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, list_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, list_monad, xs
