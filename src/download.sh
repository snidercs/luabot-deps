#!/usr/bin/bash
set -e
cd src && \
    rm *.zip* && \
    sh download-wpilib.sh && \
    sh download-phoenix6.sh
