emane-tutorial
==

The emane-tutorial is a guided walk through deploying a series of emulation
configurations and scenarios using the
[EMANE](https://github.com/adjacentlink/emane) emulator. Each demonstration in
this tutorial is designed to highlight specific capabilities of the emulator.
The tutorial provides a simple test flow using LXC Containers to create a set
of test nodes that run emulator instances along with other applications and
services typically used in the MANET world.


This project contains the configuration and scripts necessary to run the
tutorial.


The full tutorial can be found here:

  https://github.com/adjacentlink/emane-tutorial/wiki

To get started quickly in a docker environment, simply run
```bash
git clone https://adjacentlink/emane-tutorial
cd emane-tutorial/docker
docker-compose build
docker-compose up -d
ip_addr=`docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' docker_emane-tutorial_1`
ssh -YC root@${ip_addr}
```

When finished simply run
```bash
docker-compose down
```
