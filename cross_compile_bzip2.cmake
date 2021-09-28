set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# specify the cross compiler
set(CMAKE_C_COMPILER /opt/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu/bin/aarch64-none-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER /opt/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu/bin/aarch64-none-linux-gnu-g++)
set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

# where is the target environment
#set(CMAKE_FIND_ROOT_PATH /opt/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu)
set(CMAKE_FIND_ROOT_PATH /opt/ti-processor-sdk-linux-rt-j7-evm-08_00_00_08/linux-devkit/sysroots/aarch64-linux)
set(CMAKE_SYSROOT /opt/ti-processor-sdk-linux-rt-j7-evm-08_00_00_08/linux-devkit/sysroots/aarch64-linux)
#set(CMAKE_INCLUDE_PATH  /root/usr_evm/include)
#set(CMAKE_LIBRARY_PATH  /root/usr_evm/lib)
#set(CMAKE_PROGRAM_PATH  /opt/gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnu/bin)

# search for programs in the build host directories
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries and headers in the target directories
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# automatically use the cross-wrapper for pkg-config
# set(PKG_CONFIG_EXECUTABLE "/somewhere/bin/aarch64-unknown-linux-gnueabi-pkg-config" CACHE FILEPATH "pkg-config executable")
