#!/usr/bin/sh

# This installer is temporary: it installs the 'dist' folder
# to ~/wpilib/$FRC_YEAR/luabot. See also: meson.build
# WARNING: this script is destructive, the prefix directory will be
# wiped out completely.

set -e

prefix="$1"
if [ -z "$1" ];then
    prefix="${HOME}/wpilib/2025/luabot"
fi

mkdir -p "${prefix}"
rm -rf "${prefix}"
rsync -var --delete dist/ "${prefix}/"
echo
echo "Installed to ${prefix}"

exit $?
