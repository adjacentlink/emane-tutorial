#!/bin/bash
scriptdir=$(dirname "$(readlink -f "$(type -P "$0" || echo "$0")")")
set -e
trap "echo FAILED; exit 1" ERR

EMANE_RUN_DEPS=(
   checkinstall
   devscripts
   findutils
   ethtool
   iproute2
   iputils-ping
   libboost-program-options-dev
   libconfig++9v5
   libfftw3-single3
   libmbedcrypto3
   libpcap0.8
   libpcre3
   libprotobuf-dev
   libsctp1
   libsqlite3-dev
   libuhd3.15.0
   libuuid1
   lxc
   libxml2-dev
   libzmq5
   libzmq3-dev
   mgen
   openssh-server
   python-is-python3
   python3-daemon
   python3-protobuf
   python3-lxml
   python3-mako
   python3-matplotlib
   python3-numpy
   python3-pandas
   python3-paramiko
   python3-pip
   python3-protobuf
   python3-psutil
   python3-pkg-resources
   python3-pycurl
   python3-pyroute2
   python3-seaborn
   python3-tk
   python3-zmq
   sudo
   wget
   )
apt-get update -y && apt-get install -y ${EMANE_RUN_DEPS[@]} && rm -rf /var/lib/apt/lists/*


TEMP=$(mktemp)
cat << EOF > ${TEMP}
pip3 install pmw
EOF
chmod +x ${TEMP}

mkdir /pmw
checkinstall -D --pkgname="python3-pmw" --pkgversion="" --pakdir="/pmw" ${TEMP}
dpkg -i /pmw/*.deb
rm -rf /pmw
rm -rf ${TEMP}

cd /build
wget https://adjacentlink.com/downloads/emane/emane-1.3.3-release-1.ubuntu-20_04.amd64.tar.gz

tar xzf *.tar.gz
cd emane-1.3.3-release-1/debs/ubuntu-20_04/amd64
dpkg -i *.deb
rm -rf /build/emane-1.3.3-release-1

