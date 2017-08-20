#!/bin/bash

GOPATH="/opt/"
GO_VERSION="1.8.3"
GO_PKG_NAME="go${GO_VERSION}.linux-amd64.tar.gz"
GO_URL="https://storage.googleapis.com/golang/${GO_PKG_NAME}"

echo "# ----------------------------------"
echo "# -- Installing go ${GO_VERSION} from "

echo "# ---- Getting go from site ..."
cd /opt
curl ${GO_URL} > /opt/${GO_PKG_NAME}

echo "# ---- Unpackaing ${GO_PKG_NAME}"
cd /opt && /usr/bin/tar -xvzf ${GO_PKG_NAME}
rm /opt/${GO_PKG_NAME}

echo "export PATH=${PATH}:/opt/go/bin" >> /etc/skel/.bashrc
echo "export GOROOT=/opt/go" >> /etc/skel/.bashrc

echo "----------------------------------"
