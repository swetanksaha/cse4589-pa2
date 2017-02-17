#!/bin/bash
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

if [ "$#" -ne 4 ]; then
    echo "Usage: deploy HOSTNAME USER UPLOAD-PATH REMOTE-PATH"
    exit
fi

hostname=$1
user=$2
upath=$3
rpath=$4

# Package
cd C && tar -c ubitname/ -f assignment2_template_c.tar --exclude-vcs
cd ..
cd C++ && tar -c ubitname/ -f assignment2_template_cpp.tar --exclude-vcs
cd ..

# Build the grader
mkdir -p grader
./build_grader_exec.sh

# Replace hostname inside scripts
cp assignment2_init_script assignment2_init_script.sh
sed -i 's/host/'$hostname'/g' assignment2_init_script.sh
sed -i 's#remotepath#'$rpath'#g' assignment2_init_script.sh
cp assignment2_update_grader assignment2_update_grader.sh
sed -i 's/host/'$hostname'/g' assignment2_update_grader.sh
sed -i 's#remotepath#'$rpath'#g' assignment2_update_grader.sh

# Upload
scp C/assignment2_template_c.tar C++/assignment2_template_cpp.tar assignment2_init_script.sh assignment2_package.sh assignment2_update_grader.sh $user@$hostname:$upath
scp -r grader $user@$hostname:$upath/

# Cleanup
rm C/assignment2_template_c.tar
rm C++/assignment2_template_cpp.tar
rm assignment2_init_script.sh
rm assignment2_update_grader.sh
rm -rf grader/
