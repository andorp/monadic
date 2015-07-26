from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.error import error_monad, Left, Right, error_msg


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
