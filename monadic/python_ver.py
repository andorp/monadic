import sys


def get_major_version():
    version = sys.version_info
    if hasattr(version, 'major'):
        return version.major
    elif isinstance(version, tuple):
        return version[0]
    else:
        raise TypeError("Excected version_info or tuple")


PYTHON_VERSION = get_major_version()


def invalid_python_version():
    raise Exception("Invalid python version: {ver}".format(
        ver=PYTHON_VERSION))
