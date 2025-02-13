#!/bin/sh

here="$(pwd)"
root="$(pwd)"

ljdir="${root}/src/luajit"
ljbld="${here}/work/luajit"

prefix="$1"

if [ -z "$1" ]; then
    prefix="${here}/dist"
fi

set -ex

rm -rf "$ljbld"
mkdir -p "$ljbld"
rsync -ar --delete "${ljdir}/" "${ljbld}/"
cd "$ljbld"

### Build for roboRIO
export PATH="$HOME/wpilib/2025/roborio/bin:$PATH"

make amalg HOST_CC="gcc -m32 -std=c99" \
    CROSS=arm-frc2024-linux-gnueabi- \
    XCFLAGS="-DLUAJIT_ENABLE_LUA52COMPAT=1" \
    BUILDMODE="static" \
    PREFIX="$prefix"
make install PREFIX="$prefix"

find "${prefix}" -name "*luajit*.pc" -delete

cd $here

exit 0
