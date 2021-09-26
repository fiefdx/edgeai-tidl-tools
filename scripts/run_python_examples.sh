#!/bin/bash
CURDIR=`pwd`
SOCKS_PROXY=`cat ./configuration.json | python -c "import sys, json; print(json.loads(sys.stdin.read())['proxy'])"`
arch=$(uname -p)
if [[ $arch == x86_64 ]]; then
    echo "X64 Architecture"
elif [[ $arch == aarch64 ]]; then
    echo "ARM Architecture"
    $skip_arm_gcc_download=1
else
echo 'Processor Architecture must be x86_64 or aarch64'
echo 'Processor Architecture "'$arch'" is Not Supported '
return
fi

cd $CURDIR/examples/osrt_python/tfl
if [[ $arch == x86_64 ]]; then
python3 tflrt_delegate.py -c -p "$SOCKS_PROXY"
fi
python3 tflrt_delegate.py
cd $CURDIR/examples/osrt_python/ort
if [[ $arch == x86_64 ]]; then
python3 onnxrt_ep.py -c -p "$SOCKS_PROXY"
fi
python3 onnxrt_ep.py
cd $CURDIR/examples/osrt_python/tvm_dlr
if [[ $arch == x86_64 ]]; then
python3  tvm-compilation-onnx-example.py --pc-inference -p "$SOCKS_PROXY"
python3  tvm-compilation-tflite-example.py --pc-inference -p "$SOCKS_PROXY"
python3  tvm-compilation-onnx-example.py -p "$SOCKS_PROXY"
python3  tvm-compilation-tflite-example.py -p "$SOCKS_PROXY"
fi
python3  dlr-inference-example.py 
cd $CURDIR




