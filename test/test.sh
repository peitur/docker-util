#!/bin/bash

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

# Bold
BBlack='\033[1;30m'       # Black
BRed='\033[1;31m'         # Red
BGreen='\033[1;32m'       # Green
BYellow='\033[1;33m'      # Yellow
BBlue='\033[1;34m'        # Blue
BPurple='\033[1;35m'      # Purple
BCyan='\033[1;36m'        # Cyan
BWhite='\033[1;37m'       # White

# Underline
UBlack='\033[4;30m'       # Black
URed='\033[4;31m'         # Red
UGreen='\033[4;32m'       # Green
UYellow='\033[4;33m'      # Yellow
UBlue='\033[4;34m'        # Blue
UPurple='\033[4;35m'      # Purple
UCyan='\033[4;36m'        # Cyan
UWhite='\033[4;37m'       # White

# Background
On_Black='\033[40m'       # Black
On_Red='\033[41m'         # Red
On_Green='\033[42m'       # Green
On_Yellow='\033[43m'      # Yellow

PYTHONPATH="$PWD/lib:$PWD/../lib"

PYTHON3=$(which python3)
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

if [[ ! ${PYTHON3} ]]; then
  echo -e "Missing python3"
  exit
fi

DM="docker-machine"
DM_ENGINE="devtest"
DM_DRIVER="virtualbox"

DM_HOME="${HOME}/.docker"
DM_CERTS="${DM_HOME}/machine/certs"
DM_MCERTS="${DM_HOME}/machine/machines/${DM_ENGINE}"


DOCKM=$(which ${DM})
if [[ ! ${DOCKM} ]]; then
  echo -e "No ${DM}"
  exit
fi

if [[ ! $(${DM} ls ${DM_ENGINE}|grep ${DM_ENGINE}) ]]; then
  echo -e "Missing the docker machine (${DM_ENGINE} required to run tests."
  echo "${DM} create --driver ${DM_DRIVER} ${DM_ENGINE}"
fi
