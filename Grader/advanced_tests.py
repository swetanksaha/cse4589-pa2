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

parser = argparse.ArgumentParser(description='CSE 489/589 PA2: ADVANCED Tests v'+__version__)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-p', '--path', dest='path', type=str, nargs=1, help='path to your binary [abt/gbn/sr]', required=True)
requiredArgs.add_argument('-r', '--run_exp', dest='run_experiments', type=str, nargs=1, help='path to run_experiments executable', required=True)

args = parser.parse_args()

def GetAvgPackets(output_fname, Packets):
    result = open(output_fname, 'r')
    data = result.readlines()
    data.pop(0)
    result.close()

    packets = []
    for line in data:
        packets.append( float((line.split(',')[8]).rstrip('\n')) )

    if len(packets) != 10 or sum(packets) == 0.0: return False
    Packets.append(round(sum(packets)/10.0,6))

    return True

def check_monotonicity():
    diff = []
    for index in range(0,4):
        diff = (Packets[index] - Packets[index+1])/float(Packets[index])
        if diff < -0.1:
            print diff
            return False

    return True

if __name__ == '__main__':
    path = args.path[0]
    protocol = os.path.basename(path)
    utils.RUN_EXPERIMENTS_PATH = args.run_experiments[0]

    messages = '1000'
    arrival_t = '50'
    if protocol == 'abt': window = '0'
    else: window = '10'

    l_test = False
    c_test = False

    test_suite = os.path.splitext(os.path.basename(__file__))[0]
    test_name = 'GetAvgPackets'

    from test_runner import RunTest

    Packets = []
    if (RunTest(path, messages, '0.1', '0.0', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.2', '0.0', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.4', '0.0', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.6', '0.0', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.8', '0.0', arrival_t, window, test_suite, test_name, Packets)):
        # Check monotonicity
        if len(Packets) == 5 and check_monotonicity(): l_test = True

    Packets = []
    if (l_test and
        RunTest(path, messages, '0.0', '0.1', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.0', '0.2', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.0', '0.4', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.0', '0.6', arrival_t, window, test_suite, test_name, Packets) and
        RunTest(path, messages, '0.0', '0.8', arrival_t, window, test_suite, test_name, Packets)):
        # Check monotonicity
        if len(Packets) == 5 and check_monotonicity(): c_test = True

    status = False
    if l_test and c_test: status=True

    utils.print_status('ADVANCED TESTS', status)
