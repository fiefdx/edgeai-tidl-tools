#!/bin/bash

set -x -e

export HOST_ARCH=aarch64-none-linux-gnu
export TOOL_PREFIX=/opt/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu/bin/$HOST_ARCH
export CXX=$TOOL_PREFIX-g++
export CPP="$TOOL_PREFIX-g++ -E"
export AR=$TOOL_PREFIX-ar
export RANLIB=$TOOL_PREFIX-ranlib
export CC=$TOOL_PREFIX-gcc
export LD=$TOOL_PREFIX-ld
export READELF=$TOOL_PREFIX-readelf
export LDLAST="-lgcov"
export CPPFLAGS="-I$HOME/zlib/include -I$HOME/openssl/include"
export LDFLAGS="-L$HOME/zlib/lib -L$HOME/openssl/lib"

./configure --host=$HOST_ARCH --target=$HOST_ARCH --build=x86_64-pc-linux-gnu --prefix=/root/zlib LDFLAGS="-Wl,-rpath /root/zlib" --disable-ipv6 ac_cv_file__dev_ptmx=no ac_cv_file__dev_ptc=no ac_cv_have_long_long_format=yes --enable-shared --with-ensurepip=yes --enable-optimization

make BLDSHARED="$TOOL_PREFIX-gcc -shared" CROSS-COMPILE=$TOOL_PREFIX- CROSS_COMPILE_TARGET=yes

make install BLDSHARED="$TOOL_PREFIX-gcc -shared" CROSS-COMPILE=$TOOL_PREFIX- CROSS_COMPILE_TARGET=yes prefix=$HOME/Python-$HOST_ARCH/_install
