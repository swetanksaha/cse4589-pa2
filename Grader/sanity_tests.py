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

__author__ = "Swetank Kumar Saha (swetankk@buffalo.edu)"
__copyright__ = "Copyright (C) 2017 Swetank Kumar Saha"
__license__ = "GNU GPL"
__version__ = "1.0"

import argparse
import os

import utils

parser = argparse.ArgumentParser(description='CSE 489/589 PA2: SANITY Tests v'+__version__)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-p', '--path', dest='path', type=str, nargs=1, help='path to your binary [abt/gbn/sr]', required=True)
requiredArgs.add_argument('-r', '--run_exp', dest='run_experiments', type=str, nargs=1, help='path to run_experiments executable', required=True)

args = parser.parse_args()

def GetStats(data):

    Application_A = []
    Transport_A = []
    Transport_B = []
    Application_B = []

    for line in data:
        Application_A.append(int(line.split(',')[5]))
        Transport_A.append(int(line.split(',')[6]))
        Transport_B.append(int(line.split(',')[7]))
        Application_B.append(int(line.split(',')[8]))

    return Application_A, Transport_A, Transport_B, Application_B

def CheckFile(output_fname):
    result = open(output_fname, 'r')
    data = result.readlines()
    data.pop(0)
    result.close()

    Application_A, Transport_A, Transport_B, Application_B = GetStats(data)

    for index in range(0,10):
        if(Application_A[index] != 1000): return False

    return True

def Test1(output_fname):
    result = open(output_fname, 'r')
    data = result.readlines()
    data.pop(0)
    result.close()

    Application_A, Transport_A, Transport_B, Application_B = GetStats(data)

    for index in range(0,10):
        if(Application_A[index] != 20): return False
        if(Transport_B[index] > Transport_A[index]): return False
        if(Transport_B[index] < Application_B[index]): return False
        if(Application_B[index] < 18 or Application_B[index] > 20): return False

    return True

def Test2(output_fname):
    result = open(output_fname, 'r')
    data = result.readlines()
    data.pop(0)
    result.close()

    Application_A, Transport_A, Transport_B, Application_B = GetStats(data)

    for index in range(0,10):
        if(Application_A[index] != 20): return False
        if(Transport_A[index] < 21): return False
        if(Transport_B[index] != 0): return False
        if(Application_B[index] != 0): return False

    return True

def Test3(output_fname):
    result = open(output_fname, 'r')
    data = result.readlines()
    data.pop(0)
    result.close()

    Application_A, Transport_A, Transport_B, Application_B = GetStats(data)

    for index in range(0,10):
        if(Application_A[index] != 20): return False
        if(Transport_B[index] > Transport_A[index]): return False
        if(Transport_B[index] < Application_B[index]): return False
        if(Transport_B[index] < 18): return False
        if(Application_B[index] != 0): return False

    return True

if __name__=="__main__":
    path = args.path[0]
    protocol = os.path.basename(path)
    utils.RUN_EXPERIMENTS_PATH = args.run_experiments[0]

    test_suite = os.path.splitext(os.path.basename(__file__))[0]
    test_name = 'CheckFile'

    from test_runner import RunTest

    messages = '1000'
    arrival_t = '50'
    if protocol == 'abt': window = '0'
    else: window = '10'

    l_test = False
    c_test = False

    if (RunTest(path, messages, '0.1', '0.0', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.2', '0.0', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.4', '0.0', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.6', '0.0', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.8', '0.0', arrival_t, window, test_suite, test_name)):
        l_test = True

    if (l_test and
        RunTest(path, messages, '0.0', '0.1', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.0', '0.2', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.0', '0.4', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.0', '0.6', arrival_t, window, test_suite, test_name) and
        RunTest(path, messages, '0.0', '0.8', arrival_t, window, test_suite, test_name)):
        c_test = True

    messages = '20'
    if protocol == 'abt': arrival_t, window = '1000', '0'
    else: arrival_t, window = '50', '50'

    status = False
    if(l_test and c_test and
       RunTest(path, messages, '0.0', '0.0', arrival_t, window, test_suite, 'Test1') and
       RunTest(path, messages, '1.0', '0.0', arrival_t, window, test_suite, 'Test2') and
       RunTest(path, messages, '0.0', '1.0', arrival_t, window, test_suite, 'Test3')):
       status = True

    utils.print_status('SANITY TESTS', status)
