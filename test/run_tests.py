#!/usr/bin/env python3
#
# Imperialism remake
# Copyright (C) 2016 Trilarion
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Discovers all tests and runs them. Assumes that initially the working directory is test and source is not known
in the sys path.
"""

import os
import sys
import unittest


if __name__ == '__main__':
    # add source directory to path if needed
    tests_directory = os.path.abspath(os.path.dirname(__file__))
    source_directory = os.path.realpath(os.path.join(tests_directory, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    loader = unittest.defaultTestLoader

    tests = loader.discover(tests_directory)

    runner = unittest.TextTestRunner()

    results = runner.run(tests)

    # return sum of number of errors and number of failures
    sys.exit(len(results.errors) + len(results.failures))
