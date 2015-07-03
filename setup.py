# monadic's setup.py
from distutils.core import setup
setup(
    name = "monadic",
    packages = [
        "monadic",
        "monadic.monad"
        ],
    version = "1.0.0.0",
    description = "OO friendly monads in form of decorators",
    author = "Andor Penzes",
    author_email = "andor.penzes@gmail.com",
    url = "https://github.com/andorp/monadic",
    download_url = "https://github.com/andorp/monadic",
    keywords = ["functional-programing", "monad"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    long_description = """ TODO """
)
