FROM wpilib/roborio-cross-ubuntu:2025-24.04

RUN apt-get --allow-unauthenticated update && \
    apt-get install -y build-essential python3 python3-pip \
    git gcc-multilib g++-multilib luajit python3-yaml cmake \
    meson rsync

RUN pip3 install --break-system-packages \
    robotpy robotpy-build phoenix6 limelightlib-python \
    sleipnirgroup-choreolib

RUN mkdir -p /install
WORKDIR /install
COPY . ./.
RUN cd /install && sh src/download.sh && python3 deps.py && sh install.sh 
RUN cd / && rm -rf /install
WORKDIR /
