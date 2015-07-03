from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.maybe import maybe_monad, nothing, just


test_data = [
    nothing,
    just(nothing),
    just(just(nothing)),
    just(just(just(4))),
]


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, maybe_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, maybe_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, maybe_monad, xs