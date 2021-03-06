#!/usr/bin/env python

#
# Copyright (C) 2014 Simone Basso <bassosimone@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""" Integration tests for the deployed WAR """

import os
import sys
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    sys.path.insert(0, TESTS_DIR)

import integration

def main():
    """ Main function """
    integration.SETTINGS["prefix"] = ""
    unittest.main(module="integration")

if __name__ == "__main__":
    main()
