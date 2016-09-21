#!/bin/bash
PYTHONPATH="$PWD/lib:$PWD/../lib"

PYTHON3=$(which python3)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")


MODLIST="message_test.py local_test.py util_test.py"
for mod in ${MODLIST};
do
  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  echo ">>> Testing '$mod' - ${TIMESTAMP} <<<"
  $( ${PYTHON3} -m unittest ${mod} )
done
