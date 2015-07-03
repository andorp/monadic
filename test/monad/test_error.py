from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.error import error_monad, Left, Right


test_data = [
    Left("error"),
    Right(Right(Right(3))),
    Right(Left("error"))
]


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, error_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, error_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, error_monad, xs
