from monadic.monad_def import monad


class Maybe(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "(Just {value})".format(value=str(self.value))


class Nothing(Maybe):
    def __str__(self):
        return "Nothing"


nothing = Nothing()


def just(x):
    return Just(x)


def is_just(m):
    return m.__class__ is Just


def is_nothing(m):
    return m.__class__ is Nothing


def check_type(m):
    if m.__class__ in [Just, Nothing]:
        return m
    else:
        raise TypeError("Expected maybe type, found {t}".format(t=type(m)))


def maybe_functor(c):
    def fmap(m):
        check_type(m)
        if is_just(m):
            return Just(c(m.value))
        else:
            return m
    return fmap


def join(mmx):
    check_type(mmx)
    if is_nothing(mmx):
        return mmx
    else:
        return check_type(mmx.value)


def unit(x):
    return Just(x)


def maybe_monad():
    return monad(maybe_functor, join, unit)
