from monadic.functor_def import functor_law_identity, functor_law_compose
from monadic.functor_def import add1, add2
from monadic.monad_def import monad_law_one, monad_law_two, monad_law_three
from monadic.monad.none import none_monad


from nose.tools import eq_


test_data = [
    None,
    1,
    "String"
]


test_monad = none_monad()
test_functor = test_monad['t']


def test_monad_law_one():
    for xs in test_data:
        yield monad_law_one, test_monad, xs


def test_monad_law_two():
    for xs in test_data:
        yield monad_law_two, test_monad, xs


def test_monad_law_three():
    for xs in test_data:
        yield monad_law_three, test_monad, xs


functor_test_data = [
    None,
    1
]


def test_functor_law_identity():
    for x in functor_test_data:
        yield functor_law_identity, test_functor, x


def test_functor_law_compose():
    for x in functor_test_data:
        yield functor_law_compose, test_functor, add1, add2, x
