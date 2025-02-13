#!/usr/bin/sh

prefix="$1"
if [ -z "$1" ];then
    prefix="${HOME}/wpilib/2025/luabot/linuxathena"
fi

mkdir -p "${prefix}"
rm -rf "${prefix}"
rsync -var --delete dist/ "${prefix}/"
echo
echo "Installed to ${prefix}"

exit $?
