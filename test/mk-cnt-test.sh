#!/bin/bash
echo "----------------------------------"
echo "Doing the deed..."
pwd
uname -a
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
yum install -y erlang
echo "----------------------------------"
