#!/bin/bash
scriptdir=$(dirname "$(readlink -f "$(type -P "$0" || echo "$0")")")
set -e
trap "echo FAILED; exit 1" ERR

VERSION=$1

cd /build
git clone https://github.com/OLSR/olsrd
cd olsrd
git checkout v${VERSION}
make -j
for plugin in arprefresh bmf dot_draw dyn_gw dyn_gw_plain httpinfo jsoninfo mdns nameservice netjson p2pd pgraph quagga secure sgwdynspeed txtinfo watchdog
do
   echo "----------------------- $plugin -----------------------------"
   make -j $plugin
done

mkdir -p /olsrd
cd /build/olsrd
make prefix="/olsrd" -j `nproc` install

for plugin in arprefresh bmf dot_draw dyn_gw dyn_gw_plain httpinfo jsoninfo mdns nameservice netjson p2pd pgraph quagga secure sgwdynspeed txtinfo watchdog
do
   make prefix="/olsrd" -j `nproc` ${plugin}_install
done

cd /build
rm -rf /build/olsrd

