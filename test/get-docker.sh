#!/bin/bash

CURL=$( which curl )
CHMOD=$( which chmod )
GETURL="https://get.docker.com/"
INSTALLSCRIPT="/tmp/docker-install.sh"

$CURL $GETURL > $INSTALLSCRIPT
if [[ -e $INSTALLSCRIPT ]]; then
  $CHMOD +x $INSTALLSCRIPT
  $INSTALLSCRIPT
fi
