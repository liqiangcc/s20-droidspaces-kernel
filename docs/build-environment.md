# Build Environment

## Recommended host

Use a reproducible x86_64 Linux environment rather than compiling on the phone.

Recommended starting point:

```text
Ubuntu 22.04 x86_64
8 CPU cores
16 GB RAM
80 GB+ free SSD
```

WSL2 or a Linux VM can be used for source/build work, but USB/Odin/recovery operations should remain separate from the build environment.

## Baseline packages

Install only what the selected Samsung source package requires. A typical Android 4.19 kernel build host may need:

```sh
sudo apt update
sudo apt install -y \
  git build-essential bc bison flex \
  libssl-dev libelf-dev libncurses-dev \
  device-tree-compiler \
  python3 python-is-python3 \
  cpio kmod \
  lz4 xz-utils zstd \
  rsync zip unzip p7zip-full \
  curl wget libarchive-tools
```

This list is a bootstrap, not an authoritative Samsung toolchain specification.

## Toolchain rule

Do not choose Clang/GCC versions from memory or another `x1q` repository until the exact Samsung source package has been mapped. The source package README/build scripts are authoritative for the stock-baseline build.

Record exact compiler outputs such as:

```sh
clang --version
${CROSS_COMPILE}gcc --version
make --version
```

and preserve them with the build log.

## Reproducibility

A stock-baseline build should be runnable through a documented script or container once the source mapping is known. The script must pin:

- source archive/revision;
- source archive SHA256;
- toolchain version/location;
- defconfig;
- environment variables;
- build command;
- output directory.

Do not add a generic build script before Gate 1 supplies these exact values.
