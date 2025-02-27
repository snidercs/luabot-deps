echo "Usage: ./update-deps <platform> <v5_version> <v6_version>"

mkdir -p dist
cd dist
rm -rf *.zip*

set -e

wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/api-cpp/$2/api-cpp-$2-headers.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/api-cpp/$1/api-cpp-$1-linuxarm64.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/api-cpp/$1/api-cpp-$1-linuxarm32.zip
wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/api-cpp/$2/api-cpp-$2-$1.zip

wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/cci/$2/cci-$2-headers.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/cci/$1/cci-$1-linuxarm64.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/cci/$1/cci-$1-linuxarm32.zip
wget https://maven.ctr-electronics.com/release/com/ctre/phoenix/cci/$2/cci-$2-$1.zip

wget https://maven.ctr-electronics.com/release/com/ctre/phoenix6/tools/$3/tools-$3-headers.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix6/tools/$2/tools-$2-linuxarm64.zip
# wget https://maven.ctr-electronics.com/release/com/ctre/phoenix6/tools/$2/tools-$2-linuxarm32.zip
wget https://maven.ctr-electronics.com/release/com/ctre/phoenix6/tools/$3/tools-$3-$1.zip

rm -rf include
mkdir include
unzip -o api-cpp-$2-headers.zip -d include
unzip -o cci-$2-headers.zip -d include
unzip -o tools-$3-headers.zip -d include

libdir="lib/x86-64"
mkdir -p tmp "${libdir}"

unzip -o api-cpp-$2-$1.zip -d tmp
unzip -o cci-$2-$1.zip -d tmp
unzip -o tools-$3-$1.zip -d tmp

# mv tmp/linux/arm64/shared/* lib/arm64
# mv tmp/linux/arm32/shared/* lib/arm32
mv tmp/linux/x86-64/shared/* lib/x86-64
rm -rf tmp

rm *.zip*
