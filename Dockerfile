FROM ubuntu:14.04

LABEL upstream-source="https://github.com/mfvalin/rmnlib-install"
LABEL source="https://github.com/neishm/rmnlib-install-docker"

# Some dependencies needed for the server.
RUN apt-get update && apt-get install -y git make libssl-dev ksh gfortran libopenmpi-dev python liburi-perl wget libncurses5-dev libc6-dev-i386 openmpi-bin

# Create non-privileged account for compiling and installing ssm packages.
# Use the same userid and groupid as the host user to make it easier to
# mount volumes and do file I/O with the host system.
RUN groupadd -g 1000 ssm
RUN useradd -g ssm -u 1000 -m ssm

USER ssm

# Use rmnlib-install to build the core packages.
WORKDIR /home/ssm
RUN git clone https://github.com/mfvalin/rmnlib-install.git 
WORKDIR /home/ssm/rmnlib-install
RUN git fetch && git checkout 7abaa4ea96713c99d6eb140136fa6bccf423caf8
RUN make auto-install

# Set up the environment to load at login time.
WORKDIR /home/ssm
RUN echo . /home/ssm/ssm-domains-base/ssm_10.151/etc/ssm.d/profile >> .profile
RUN echo . env-setup.dot >> .profile
RUN echo . r.load.dot /home/ssm/ssm-domains-base/lib >> .profile