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

import subprocess
import signal
import os
import random
import string

from utils import *

TIMEOUT = 180 * 2 #6 minutes

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

def RunTest(path, messages, loss, corruption, arrival_t, window, test_suite, test_func, *arglist):
    print_regular('Testing with MESSAGES:%s, LOSS:%s, CORRUPTION:%s, ARRIVAL:%s, WINDOW:%s ...' % (messages, loss, corruption, arrival_t, window))

    output_fname = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    delete_file(output_fname)
    if not os.path.isfile(path):
        print_error('%s: File does not exist!' % (path))
        return False

    command = [RUN_EXPERIMENTS_PATH, '-m', messages,
                                     '-l', loss,
                                     '-c', corruption,
                                     '-t', arrival_t,
                                     '-w', window,
                                     '-p', path,
                                     '-o', output_fname]

    signal.signal(signal.SIGALRM, alarm_handler)
    run_expr_proc = subprocess.Popen(command)
    signal.alarm(TIMEOUT)
    try:
        run_expr_proc.wait()
        ret_code = run_expr_proc.returncode
        if ret_code != 0:
            print_error('Program terminated with non-zero exit code!')
            return False
        signal.alarm(0)
    except Alarm:
        print_error('FAIL: Your implementation failed to produce output within: %ss!' % (TIMEOUT))
        run_expr_proc.kill()
        delete_file(output_fname)
        return False

    try:
        test_suite = __import__(test_suite)
        if getattr(test_suite, test_func)(output_fname, *arglist):
            print_success('PASS!')
            return True
        else:
            print_error('FAIL: Results did NOT match expected values!')
            return False
    except Exception, e:
        print str(e)
        print_error('FAIL: Unable to grade!')
        return False
    finally:
        delete_file(output_fname)
