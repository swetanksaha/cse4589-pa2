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
import subprocess

from utils import *

parser = argparse.ArgumentParser(description='CSE 489/589 PA2: Run Experiments v'+__version__)

parser.add_argument('-o', '--output-file', dest='file', type=str, nargs=1, help='path to output file [default: results.csv]')
parser.add_argument('-n', '--no-header', dest='header', help='suppress the header in the outputfile', action='store_false')
parser.set_defaults(file=['results.csv'], header=True)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-m', '--messages', dest='messages', type=int, nargs=1, help='number of messages to simulate', required=True)
requiredArgs.add_argument('-l', '--loss', dest='loss', type=float, nargs=1, help='packet loss probability', required=True)
requiredArgs.add_argument('-c', '--corruption', dest='corruption', type=float, nargs=1, help='packet corruption probability', required=True)
requiredArgs.add_argument('-t', '--time', dest='time', type=float, nargs=1, help='average time between message generation', required=True)
requiredArgs.add_argument('-w', '--window', dest='window', type=int, nargs=1, help='window size for gbn/sr [supply 0 for abt]', required=True)
requiredArgs.add_argument('-p', '--path', dest='path', type=str, nargs=1, help='path to your binary [abt/gbn/sr]', required=True)

args = parser.parse_args()

def write_header_to_file(filename):
    result_file = open(filename, 'a+')
    err = False
    try:
        header = "Run,Messages,Loss,Corruption,Time_bw_messages,Application_A,Transport_A,Transport_B,Application_B,Total_time,Throughput\n"
        result_file.write(header)
    except:
        print_error('Failed to write header to file: %s' % (filename))
        delete_file(filename)
        err = True
    finally:
        result_file.close()
        if err: sys.exit(1)

def write_result_to_file(run, param_string, ouptut, filename):
    result_file = open(filename, 'a+')
    err = False
    try:
        for item in output.split("\n"):
            if "packets sent from the Application Layer of Sender A[/PA2]" in item:
                application_A = item.split(' ')[0].replace('[PA2]','')
            if "packets sent from the Transport Layer of Sender A[/PA2]" in item:
                transport_A = item.split(' ')[0].replace('[PA2]','')
            if "packets received at the Transport layer of Receiver B[/PA2]" in item:
                transport_B = item.split(' ')[0].replace('[PA2]','')
            if "packets received at the Application layer of Receiver B[/PA2]" in item:
                application_B = item.split(' ')[0].replace('[PA2]','')
            if "[PA2]Total time: " in item:
                time = item.split(' ')[2]
            if "[PA2]Throughput: " in item:
                throughput = item.split(' ')[1]

        result_string = ','.join([application_A, transport_A, transport_B, application_B, time, throughput])
        result_file.write(str(run)+','+param_string+','+result_string+'\n')
    except:
        print_error('Failed to parse results OR write results to file')
        delete_file(filename)
        err = True
    finally:
        result_file.close()
        if err: sys.exit(1)

if __name__ == "__main__":
    print 'Running simulator [10 Runs] ...'

    if(args.header): write_header_to_file(args.file[0])
    param_string = str(args.messages[0])+','+str(args.loss[0])+','+str(args.corruption[0])+','+str(args.time[0])

    seed_list = [1234, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]
    run = 1
    for seed in seed_list:
        print_regular('Run#'+str(run)+' [seed=%s] ... ' % (str(seed)), newline=False)

        command = [args.path[0], '-s', str(seed),
                                 '-w', str(args.window[0]),
                                 '-m', str(args.messages[0]),
                                 '-l', str(args.loss[0]),
                                 '-c', str(args.corruption[0]),
                                 '-t', str(args.time[0]),
                                 '-v', '0']
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            print_error('Error Code:')
            print exc.returncode
            print_error(exc.output)
            sys.exit(1)

        write_result_to_file(run, param_string, output, args.file[0])

        print_success('Done!')
        run += 1
