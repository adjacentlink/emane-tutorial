from ubuntu:20.04 as OLSR

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y \
      bison \
      build-essential \
      checkinstall \
      cmake \
      debian-builder \
      devscripts \
      dh-systemd \
      flex \
      git \
      libgps-dev \
      libnl-3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY docker/build_olsrd.sh .
RUN ./build_olsrd.sh 0.9.8

from ubuntu:20.04 as EMANE_TUTORIAL

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=OLSR /olsrd/ /usr
# RUN dpkg -i /olsrd/*.deb
# RUN cp -r /olsrd/* /usr/

WORKDIR /build

COPY docker/install_emane.sh .
RUN ./install_emane.sh

COPY . /emane-tutorial

WORKDIR /emane-tutorial
RUN rm -rf .git && rm -rf docker && make

#####################################################################
# Setup ssh service
RUN mkdir /var/run/sshd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config
RUN echo "TCPKeepAlive  yes" >> /etc/ssh/sshd_config
RUN sed -ri 's/.*X11UseLocalhost.*/X11UseLocalhost no/' /etc/ssh/sshd_config
RUN sed -ri 's/^UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

# Delete root password (set as empty)
RUN passwd -d root

# Create shared key for logging into lxc containers
#RUN ssh-keygen -P "" -f /root/.ssh/id_rsa \
#    && cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN echo "cd /emane-tutorial" >> /root/.bashrc
#####################################################################

# Setup x11 support
RUN apt-get update && apt-get install -y \
       x11-common \
    && rm -rf /var/lib/apt/lists/*

CMD ["/usr/sbin/sshd", "-D"]
