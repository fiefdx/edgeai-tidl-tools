#!/bin/bash
cmd_path=$(dirname $0)
cd $cmd_path
SOCKS_PROXY=`cat ./configuration.json | python3 -c "import sys, json; print(json.loads(sys.stdin.read())['proxy'])"`
arch=$(uname -p)

if [[ -z "$TIDL_TOOLS_PATH" ]]
then
cd tidl_tools
export TIDL_TOOLS_PATH=$(pwd)
cd ..
fi

if [[ $arch == x86_64 ]]; then
    echo "X64 Architecture"
    export LD_LIBRARY_PATH=$TIDL_TOOLS_PATH
fi
