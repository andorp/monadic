from monadic.monad_def import monad


class Either(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Left(Either):
    def __init__(self, msg):
        self.left = msg

    def __str__(self):
        return "Left ({x})".format(x=self.left)


class Right(Either):
    def __init__(self, x):
        self.right = x

    def __str__(self):
        return "Right ({x})".format(x=self.right)


def check_type(x):
    if x.__class__ in [Left, Right]:
        return x
    else:
        raise TypeError("Expected either type, found {v}:{t}".format(v=x, t=x.__class__))


def isLeft(x):
    return x.__class__ is Left


def error_functor(f):
    def fmap(e):
        check_type(e)
        if isLeft(e):
            return e
        else:
            return Right(f(e.right))
    return fmap


def join(e):
    check_type(e)
    if isLeft(e):
        return e
    else:
        return check_type(e.right)


def error_msg(msg):
    return Left(msg)


def error_monad():
    return monad(error_functor, join, Right)
