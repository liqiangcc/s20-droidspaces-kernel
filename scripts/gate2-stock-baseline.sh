#!/usr/bin/env bash
set -euo pipefail

# Experimental Gate 2 build for the reconstructed SM-G9810/x1q China source.
# This script only configures or compiles the kernel. It never creates a boot
# image and never communicates with the phone.

phase="${1:-all}"
case "$phase" in
  config|build|all) ;;
  *) echo "usage: $0 [config|build|all]" >&2; exit 2 ;;
esac

analysis_root="${ANALYSIS_ROOT:-/mnt/d/codex-source-analysis/s20-20260823}"
repo_root="${REPO_ROOT:-/mnt/c/Users/liqia/Downloads/platform-tools-latest-windows/s20-droidspaces-kernel}"
source_dir="${SOURCE_DIR:-$analysis_root/build/source}"
out_dir="${OUT_DIR:-$analysis_root/build/out-stock}"
log_dir="${LOG_DIR:-$analysis_root/build/logs}"
sdllvm_dir="${SDLLVM_DIR:-$analysis_root/toolchains/sdllvm-10.0.9}"
gcc_dir="${GCC_DIR:-$analysis_root/toolchains/aarch64-linux-android-4.9}"
compat_dir="${COMPAT_DIR:-$analysis_root/toolchains/compat-libtinfo5/lib/x86_64-linux-gnu}"
python2_bin="${PYTHON2_BIN:-/usr/bin/python2}"
stock_config="${STOCK_CONFIG:-$repo_root/evidence/stock.config}"
source_archive="${SOURCE_ARCHIVE:-$analysis_root/candidate/SM-G9810_X1Q_CHN_HXJ2_RECONSTRUCTED_v3_Kernel.tar.gz}"
jobs="${JOBS:-$(nproc)}"
host_tools="${HOST_TOOLS:-$out_dir/host-tools}"

clang="$sdllvm_dir/bin/clang"
cross_compile="$gcc_dir/bin/aarch64-linux-android-"
dtc="$source_dir/tools/dtc"

for required in "$source_dir/Makefile" "$stock_config" "$clang" "$dtc" "$python2_bin" \
  "${cross_compile}elfedit"; do
  if [[ ! -e "$required" ]]; then
    echo "required path missing: $required" >&2
    exit 1
  fi
done

mkdir -p "$out_dir" "$log_dir" "$host_tools"
ln -sfn "$python2_bin" "$host_tools/python"
ln -sfn "$python2_bin" "$host_tools/python2"
export PATH="$host_tools:$PATH"
export LD_LIBRARY_PATH="$compat_dir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export ARCH=arm64
export KBUILD_BUILD_USER=codex-gate2
export KBUILD_BUILD_HOST=wsl2
export KBUILD_BUILD_VERSION=1
export KBUILD_BUILD_TIMESTAMP='Tue Oct 15 12:52:48 KST 2024'
export LC_ALL=C

make_args=(
  -C "$source_dir"
  O="$out_dir"
  DTC_EXT="$dtc"
  CONFIG_BUILD_ARM64_DT_OVERLAY=y
  ARCH=arm64
  CROSS_COMPILE="$cross_compile"
  REAL_CC="$clang"
  CLANG_TRIPLE=aarch64-linux-gnu-
  PYTHON=python3
)

# Samsung's recursive Makefiles do not preserve REAL_CC and PYTHON through
# every sub-make. Recreate the tree-local paths named by README_Kernel.txt;
# these links exist only in the disposable D: build tree.
mkdir -p "$source_dir/toolchain/llvm-arm-toolchain-ship"
mkdir -p "$source_dir/toolchain/gcc/linux-x86/aarch64"
ln -sfn "$sdllvm_dir" "$source_dir/toolchain/llvm-arm-toolchain-ship/10.0"
ln -sfn "$gcc_dir" \
  "$source_dir/toolchain/gcc/linux-x86/aarch64/aarch64-linux-android-4.9"

record_versions() {
  {
    if [[ -f "$source_archive" ]]; then
      echo "source_archive=$(basename "$source_archive")"
      echo "source_archive_sha256=$(sha256sum "$source_archive" | awk '{print $1}')"
    else
      echo "source_archive=unavailable:$source_archive"
    fi
    echo "sdllvm_commit=b31ec4293cb8a1a634a74756929ed47997629665"
    echo "sdllvm_archive_sha256=483c012c87694738a0788b968b5b1b3551ea1968eda978f19e74d93ae07a519b"
    echo "gcc_commit=$(git -C "$gcc_dir" rev-parse HEAD)"
    echo "libtinfo5_deb_sha256=b9bb64e716a7d9de05b1b33992763142ca81bcae3a7f8ce7e29fa3c6fd32f1e8"
    "$clang" --version
    "${cross_compile}gcc-4.9.x" --version | head -1
    "${cross_compile}ld" --version | head -1
    "$dtc" --version
    "$python2_bin" --version 2>&1
    make --version | head -1
    uname -a
  } > "$log_dir/toolchain-versions.txt"
}

configure() {
  cp "$stock_config" "$out_dir/.config"
  cp "$stock_config" "$log_dir/stock.config.before-olddefconfig"
  make "${make_args[@]}" olddefconfig 2>&1 | tee "$log_dir/olddefconfig.log"
  cp "$out_dir/.config" "$log_dir/stock.config.after-olddefconfig"
  diff -u "$stock_config" "$out_dir/.config" > "$log_dir/stock-config.diff" || true
  "$source_dir/scripts/diffconfig" "$stock_config" "$out_dir/.config" \
    > "$log_dir/stock-config.semantic.diff" || true
  sha256sum "$stock_config" "$out_dir/.config" \
    > "$log_dir/config-sha256.txt"
}

build_kernel() {
  if [[ ! -f "$out_dir/.config" ]]; then
    echo "missing $out_dir/.config; run config phase first" >&2
    exit 1
  fi
  make -j"$jobs" "${make_args[@]}" 2>&1 | tee "$log_dir/build.log"
  image="$out_dir/arch/arm64/boot/Image"
  if [[ ! -s "$image" ]]; then
    echo "kernel Image was not produced: $image" >&2
    exit 1
  fi
  sha256sum \
    "$image" \
    "$out_dir/arch/arm64/boot/Image-dtb" \
    "$out_dir/vmlinux" \
    "$out_dir/System.map" \
    "$out_dir/.config" \
    > "$log_dir/artifact-sha256.txt"
  "$source_dir/scripts/extract-ikconfig" "$image" \
    > "$log_dir/Image.embedded.config"
  cmp "$out_dir/.config" "$log_dir/Image.embedded.config"
  if [[ -f "$out_dir/certs/signing_key.x509" ]]; then
    sha256sum "$out_dir/certs/signing_key.x509" \
      > "$log_dir/signing-certificate-sha256.txt"
  fi
  find "$out_dir" -type f -name '*.ko' -print0 | sort -z \
    | xargs -0 -r sha256sum > "$log_dir/module-sha256.txt"
}

record_versions
if [[ "$phase" == config || "$phase" == all ]]; then
  configure
fi
if [[ "$phase" == build || "$phase" == all ]]; then
  build_kernel
fi
