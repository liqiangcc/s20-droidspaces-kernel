# Experimental Gate 2 Stock-Baseline Evidence

Captured: 2026-08-24 (Asia/Shanghai)

## Status and scope

The owner explicitly authorized an experimental Gate 2 build despite the
unresolved exact-release requirement recorded by Gate 1. The reconstructed
source compiles through Samsung CFP instrumentation, FIPS HMAC injection,
kernel image generation, and module linking.

```text
formal Gate 1 = BLOCKED (exact SM-G9810 G9810ZCSBHXJ2 OSRC release unavailable)
experimental Gate 2 = build successful; same-output-tree rebuild is reproducible
formal Gate 2 = BLOCKED by Gate 1 and by clean-tree signing-key reproducibility
```

No boot image was created or unpacked. No ADB write, Odin, Heimdall, flashing,
or block-device command was run.

## Reconstructed source v3

```text
artifact: D:\codex-source-analysis\s20-20260823\candidate\SM-G9810_X1Q_CHN_HXJ2_RECONSTRUCTED_v3_Kernel.tar.gz
size: 212190213 bytes
SHA256: b8f997f84ef48d38b3d4ca1e848eb099be261ffd084c459f188ed482d8bf4dc7
entries: 70952
```

The source recipe remains the documented KOR IXJ1 x1q base, official HK x1q
China project files, and official CHN HXJ2 regional common files. Version v3
also explicitly routes these case-colliding netfilter paths through the CHN
archive:

```text
include/uapi/linux/netfilter/xt_mark.h
include/uapi/linux/netfilter/xt_dscp.h
net/netfilter/xt_dscp.c
```

Archive-level comparison still reports the same six changed common files as
v1 because the exact lowercase netfilter members are byte-identical in the KOR
and CHN tar archives. The explicit routing prevents a Windows-extracted,
case-collapsed copy from being mistaken for an authoritative member.

## Filesystem finding

The first build directory on `D:` was not case-sensitive. Linux netfilter uses
distinct names such as `xt_DSCP.c` and `xt_dscp.c`; NTFS/DrvFS collapsed them.
This first appeared as missing/incomplete `xt_mark` and `xt_dscp` build inputs.
Direct tar-archive comparison showed that Samsung's archives contain the
lowercase members; the apparent omission was caused by extraction, not by the
official source package.

The authoritative build therefore used the WSL ext4 paths:

```text
source: /home/liqiang/codex-build-s20-20260823/source
output: /home/liqiang/codex-build-s20-20260823/out-stock
logs:   /home/liqiang/codex-build-s20-20260823/logs
```

Both `net/netfilter/xt_DSCP.c` and `net/netfilter/xt_dscp.c` were observed in
that source tree, and both `xt_mark.o` and `xt_dscp.o` compiled successfully.

## Configuration result

`evidence/stock.config` was copied directly to the output `.config`, then
Samsung's source was run through `olddefconfig`.

```text
captured stock.config SHA256:
6c2ca2e3350edfa93be82f34861832397eb6a1d43c9661308a8b15a4afcbdaf

post-olddefconfig .config SHA256:
6ee315fb3486bf815aa6853e61c7d206a2d5cdfc7e51fcb41dbe6ab0786381fe
```

The semantic diff is limited to 16 explicitly disabled selectors being
removed and the observed compiler metadata changing from Clang 10.0.6 to the
available 10.0.9 toolchain:

```text
CONFIG_CLANG_VERSION: 100006 -> 100009
```

`CONFIG_MACH_X1Q_CHN_OPEN=y`, Samsung DEFEX/FIVE/PROCA settings, and all
captured namespace settings remain unchanged. The config extracted from the
built Image has the same SHA256 as the post-`olddefconfig` `.config`; semantic
diff is empty.

## Toolchain actually used

```text
Clang: Snapdragon LLVM ARM Compiler 10.0.9
Clang source commit: b31ec4293cb8a1a634a74756929ed47997629665
Clang archive SHA256: 483c012c87694738a0788b968b5b1b3551ea1968eda978f19e74d93ae07a519b

GCC cross tools: aarch64-linux-android GCC 4.9.x 20150123 prerelease
GCC repository commit: 961622e926a1b21382dba4dd9fe0e5fb3ee5ab7c
GNU ld: binutils-2.27-41d8fcb, 2.27.0.20170315
DTC: 1.4.4-Android-build
Python for Samsung CFP: 2.7.18
Python source archive SHA256: da3080e3b488f648a3d7a4560ddee895284c3380b11d6de75edb986526b9a814
libtinfo5 compatibility package SHA256: b9bb64e716a7d9de05b1b33992763142ca81bcae3a7f8ce7e29fa3c6fd32f1e8
```

The exact stock compiler was Clang 10.0.6. No public copy of Samsung's exact
10.0.6 toolchain was established, so the 10.0.9 substitution remains an
explicit mismatch.

## Build invocation

The reproducible wrapper is `scripts/gate2-stock-baseline.sh`. The successful
run used:

```sh
SOURCE_DIR=/home/liqiang/codex-build-s20-20260823/source \
OUT_DIR=/home/liqiang/codex-build-s20-20260823/out-stock \
LOG_DIR=/home/liqiang/codex-build-s20-20260823/logs \
PYTHON2_BIN=/home/liqiang/codex-build-s20-20260823/python2-host/install/bin/python2.7 \
JOBS=12 \
/mnt/c/Users/liqia/Downloads/platform-tools-latest-windows/s20-droidspaces-kernel/scripts/gate2-stock-baseline.sh build
```

The wrapper fixes `KBUILD_BUILD_VERSION=1`, build user/host, and the observed
stock timestamp. It invokes only kernel configuration/build commands and does
not package or flash anything.

## Successful artifacts

First fixed-`#1` build:

```text
Image size: 51953676 bytes
Image SHA256: f8148e92890078faaf8a0ab03c370f43e4850f0cac9a7c2769419a71c50f991e
version: Linux version 4.19.113 (codex-gate2@wsl2) (clang version 10.0.9) #1 SMP PREEMPT Tue Oct 15 12:52:48 KST 2024
vmlinux SHA256: fddc741b85bd2fbbd4d4d8fc88926d7b109228c2467bda8a2fccf0d973d64bb4
System.map SHA256: 33082331d5cc614015dae2edf340841bd60b50ce2fb52664323ca1e3a40b270d
Image-dtb SHA256: f1092e4f2d04f113b7e62a7a91aa245b206fb3cb4d224e12442a818886a39381
generated signing certificate SHA256: 58fb0fd180deb9b4e94e0f318ca657e37aa105a9f03d66520f879ee17be23e46
```

A second build using the same source, output tree, toolchain, signing key,
fixed build number, and fixed timestamp completed successfully. Its hashes are
byte-identical:

```text
Image SHA256: f8148e92890078faaf8a0ab03c370f43e4850f0cac9a7c2769419a71c50f991e
vmlinux SHA256: fddc741b85bd2fbbd4d4d8fc88926d7b109228c2467bda8a2fccf0d973d64bb4
System.map SHA256: 33082331d5cc614015dae2edf340841bd60b50ce2fb52664323ca1e3a40b270d
Image-dtb SHA256: f1092e4f2d04f113b7e62a7a91aa245b206fb3cb4d224e12442a818886a39381
```

This proves incremental/same-key reproducibility. It does not prove clean-tree
reproducibility because a fresh output tree generates a new signing key.

Four modules were generated and checksummed in the external log directory:

```text
drivers/media/usb/gspca/gspca_main.ko
drivers/mmc/core/mmc_test.ko
net/ipv4/tcp_htcp.ko
net/ipv4/tcp_westwood.ko
```

## Warnings and unresolved risk

- Exact Gate 1 source identity remains unresolved; this is a reconstructed
  candidate, not a Samsung-issued SM-G9810 HXJ2 package.
- Clang 10.0.9 differs from the phone's observed Clang 10.0.6.
- Samsung's internal `secgetspf` command is absent, so SEP/product feature
  metadata could not be reproduced.
- The full Android tree's `system/core/liblog/include/log/perflog.h` is absent;
  Samsung's kperfmon Makefile used its documented dummy/fallback path.
- DTC emits numerous warnings from the released Samsung DTS files.
- `gsi_write_channel_scratch` module-version generation warns that the export
  will not be versioned.
- A local random module-signing key was generated in the disposable output
  tree. It is not committed and must not be treated as a production key. A
  clean output tree would generate a different key and therefore a different
  built-in certificate/Image; this prevents formal clean-tree reproducibility.
- The older HK provenance of the x1q China DTS remains the largest device-risk
  item. A successful compile cannot prove that it is safe to boot.

Gate 3 must not begin until the owner reviews these residual risks and a stock
boot backup/restore procedure is independently verified.
