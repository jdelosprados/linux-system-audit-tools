# Uses an ESET script to search for cdorked infections.

#!/bin/bash

# Jump into tmp
cd /tmp

# Get the source from ESET
wget http://www.welivesecurity.com/wp-content/uploads/2013/04/dump_cdorked_config.c -O dump_cdorked_config.c -q

# Make sure we have GCC available
if [ "$(which gcc 2>&1 > /dev/null ; echo $?)" != "0" ]; then
  echo "GCC is not installed.  Please install it before running this script";
  echo "  Debian: sudo apt-get install build-essential";
  echo "  Fedora: sudo yum groupinstall \"Development Tools\"";
  exit 1;
fi;

# Build the lib
gcc -o dump_cdorked_config dump_cdorked_config.c

# check if building the tool worked
if [ "$?" != "0" ]; then
  echo "Building the tool failed... :(";
  exit 1;
fi;

# Run the tool
./dump_cdorked_config