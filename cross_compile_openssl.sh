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

./Configure linux-aarch64 --prefix=$HOME/openssl --openssldir=$HOME/openssl

make

make install
