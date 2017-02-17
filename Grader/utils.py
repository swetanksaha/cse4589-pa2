#!/usr/bin/python
#
# This file is part of CSE 489/589 Grader.
#
# CSE 489/589 Grader is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# CSE 489/589 Grader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CSE 489/589 Grader. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import subprocess

RUN_EXPERIMENTS_PATH = ''

def print_generic(print_str, newline):
    if newline: print print_str
    else: print print_str,
    sys.stdout.flush()

def print_regular(text, newline=True):
    print_str = '\033[33m%s\033[0m' % (text)
    print_generic(print_str, newline)

def print_success(text, newline=True):
    print_str = '\033[92m%s\033[0m' % (text)
    print_generic(print_str, newline)

def print_error(text, newline=True):
    print_str = '\033[91m%s\033[0m' % (text)
    print_generic(print_str, newline)

def print_note(text, newline=True):
    print_str = '\033[4mNOTE:\033[0m %s' % (text)
    print_generic(print_str, newline)

def print_status(test_suite, status):
    print '%s: ' % (test_suite),
    if status: print_success('PASS')
    else:
        print_error('FAIL')
        print_note('ALL sub-tests should show PASS status for %s to pass.' % (test_suite))

def delete_file(filepath):
    subprocess.call(['rm', filepath], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
