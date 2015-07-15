#!/bin/sh

# Test cases with coverage
nosetests test/monad --with-coverage --cover-html --cover-erase --cover-package=monadic --nocapture
