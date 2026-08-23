# Gate 1 Source-Mapping Evidence

Captured/reviewed: 2026-08-23 (Asia/Shanghai)

## Result

```text
Gate 1 = BLOCKED
```

Reason: Samsung OSRC returned no release for the exact firmware
`G9810ZCSBHXJ2`; available official and third-party candidates have an unresolved
model, region, release, or provenance mismatch.

## Samsung official observations

### Exact firmware

URL:
https://opensource.samsung.com/uploadSearch?searchValue=G9810ZCSBHXJ2

Observed browser text:

```text
This is the result of your ‘G9810ZCSBHXJ2’. 0 of results found.
Result : 0
No results has been uploaded in this category.
```

### Exact model

URL:
https://opensource.samsung.com/uploadSearch?searchValue=SM-G9810

Observed browser fields:

```text
Result: 1
Classification: Mobile Phone
Model: SM-G9810
Version: G9810ZHU6HWH9
Description: SM-G9810_HK_13_Opensource.zip
Source popup uploadId: 11969
```

### Same build suffix, different model

URL:
https://opensource.samsung.com/uploadSearch?searchValue=G9860ZCSBHXJ2

Observed browser fields:

```text
Result: 1
Classification: Mobile Phone
Model: SM-G9860
Version: G9860ZCSBHXJ2
Description: SM-G9860_CHN_13_Opensource.zip
Source popup uploadId: 12985
```

### Firmware release corroboration

URL:
https://doc.samsungmobile.com/SM-G9810/011974200319/eng.html

Relevant official fields:

```text
Galaxy S20 5G (SM-G9810)
Build Number: G9810ZCSBHXJ2
Android version: T (Android 13)
Release Date: 2024-10-28
Security patch level: 2024-09-01
```

## Archive/checksum status

```text
Exact matching Samsung archive: not identified
Downloaded exact matching archive: no
Exact matching archive SHA256: unavailable
Downloaded sibling archive: SM-G9860_CHN_13_Opensource.zip
Sibling archive size: 254544062 bytes
Sibling archive SHA256: d3595efa1f00a60768958b1fbc95703c954cb3997f11b1ca66ef318a7734c87c
ZIP full-read result: OK (4 entries, 257395387 uncompressed bytes)
```

The exact firmware query still returns zero results. The SM-G9860 archive was
downloaded as first-party sibling evidence, not treated as an exact match.

## Official sibling archive inspection

Top-level ZIP entries read:

```text
Kernel.tar.gz
Platform.tar.gz
README_Kernel.txt
README_Platform.txt
```

Files actually extracted/read from `Kernel.tar.gz`:

```text
Makefile
arch/arm64/configs/vendor/y2q_chn_openx_defconfig
arch/arm64/boot/dts/samsung/y2q/Makefile
```

Archive path scan:

```text
total paths: 76067
paths containing x1q (case-insensitive): 0
vendor defconfigs: arch/arm64/configs/vendor/y2q_chn_openx_defconfig
```

README build identity:

```text
ARCH=arm64
defconfig=vendor/y2q_chn_openx_defconfig
DTC_EXT=tools/dtc
CONFIG_BUILD_ARM64_DT_OVERLAY=y
CLANG_TRIPLE=aarch64-linux-gnu-
output=arch/arm64/boot/Image
```

README/Makefile toolchain evidence:

```text
CROSS_COMPILE=<android platform>/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-
REAL_CC=toolchain/llvm-arm-toolchain-ship/10.0/bin/clang
CLANG_TRIPLE=aarch64-linux-gnu-
VERSION=4
PATCHLEVEL=19
SUBLEVEL=113
```

Identity comparison:

```text
stock config:     CONFIG_MACH_X1Q_CHN_OPEN=y
G9860 defconfig:  CONFIG_MACH_Y2Q_CHN_OPEN=y
x1q China-open defconfig in archive: absent
```

The namespace subset and `CONFIG_WLAN_REGION_CODE=300` agree with stock, and
both configs record Clang 10.0.6, but those common values do not override the
x1q/y2q device mismatch. Gate 1 remains blocked.

## Auxiliary source tree inspection

Repository:
https://github.com/xwenx90/GalaxyS20_Series_KernelSU_Next_Susfs

```text
commit=882a4b75dffcf400aa4dbb3fcf739d988c1a64e0
branch=x1q
declared region=Korea
declared kernel=4.19.113
declared base=Android 13 / One UI 5.1
```

Files read:

```text
README.md
build_kernel.sh
Makefile
arch/arm64/configs/vendor/x1q_kor_singlex_defconfig
```

No `G9810`, `G9860`, or exact firmware identifier was found in those inspected
paths.

Makefile version fields:

```text
VERSION = 4
PATCHLEVEL = 19
SUBLEVEL = 113
EXTRAVERSION =
```

Build-script fields:

```text
ARCH=arm64
BUILD_CROSS_COMPILE=toolchain/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-
KERNEL_LLVM_BIN=toolchain/llvm-arm-toolchain-ship/10.0/bin/clang
CLANG_TRIPLE=aarch64-linux-gnu-
KERNEL_MAKE_ENV="DTC_EXT=tools/dtc CONFIG_BUILD_ARM64_DT_OVERLAY=y"
O=out
defconfig=vendor/x1q_kor_singlex_defconfig
output=out/arch/arm64/boot/Image
```

## Defconfig comparison evidence

Parsed-symbol counts:

```text
stock_symbols=5805
candidate_symbols=5780
changed_common=12
stock_only=41
candidate_only=16
```

All common-symbol value differences found by the direct text comparison:

```text
CONFIG_CFP: stock=y; candidate=<not set>
CONFIG_FIVE: stock=y; candidate=<not set>
CONFIG_INTEGRITY_TRUSTED_KEYRING: stock=y; candidate=y[trailing space]
CONFIG_MACH_X1Q_CHN_OPEN: stock=y; candidate=<not set>
CONFIG_MACH_X1Q_KOR_SINGLE: stock=<not set>; candidate=y
CONFIG_MPTCP: stock=<not set>; candidate=y
CONFIG_PROCA: stock=y; candidate=<not set>
CONFIG_SECURITY_DEFEX: stock=y; candidate=<not set>
CONFIG_SECURITY_DSMS: stock=y; candidate=<not set>
CONFIG_SUPPORT_MCC_THRESHOLD_CHANGE: stock=<not set>; candidate=y
CONFIG_UH: stock=y; candidate=<not set>
CONFIG_WLAN_REGION_CODE: stock=300; candidate=200
```

Additional source-only/stock-only security evidence:

```text
CONFIG_KDP_CRED: stock=y; candidate=<absent>
CONFIG_KDP_DMAP: stock=y; candidate=<absent>
CONFIG_KDP_NS: stock=y; candidate=<absent>
CONFIG_KSU: stock=<absent>; candidate=y
CONFIG_KSU_SUSFS: stock=<absent>; candidate=y
```

Namespace subset:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
# CONFIG_USER_NS is not set
# CONFIG_PID_NS is not set
CONFIG_NET_NS=y
# CONFIG_VETH is not set
CONFIG_IPC_NS line: absent
```

## Toolchain evidence boundary

Directly observed in `evidence/stock.config`:

```text
Compiler: clang version 10.0.6 for Android NDK
CONFIG_GCC_VERSION=0
CONFIG_CC_IS_CLANG=y
CONFIG_CLANG_VERSION=100006
```

Observed only in the auxiliary build script:

```text
Clang directory: llvm-arm-toolchain-ship/10.0
GCC cross compiler: aarch64-linux-android-4.9
CLANG_TRIPLE: aarch64-linux-gnu-
```

The exact Samsung toolchain archive/revision remains unverified.

## Commands deliberately not executed

```text
make
make defconfig
make olddefconfig
clang
kernel compilation
boot image extraction/repacking
Odin
Heimdall
dd
```
