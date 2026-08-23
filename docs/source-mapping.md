# Source Mapping

## Gate 1 status: BLOCKED

No Samsung Open Source Release Center entry was found for the phone's exact
firmware identifier `G9810ZCSBHXJ2`. Gate 1 therefore does not pass, and Gate 2
must not start.

The blocking mismatch is not cosmetic:

- the only OSRC result for the exact model `SM-G9810` is an older Hong Kong
  release, `G9810ZHU6HWH9`;
- an OSRC package exists with the same `ZCSBHXJ2` suffix, but it is published
  for `SM-G9860` (Galaxy S20+), not `SM-G9810`;
- the auxiliary source tree that was available for direct inspection contains
  only a Korean x1q defconfig, while the phone's stock config explicitly selects
  the China-open machine configuration.

No kernel was configured or compiled, and no image command was executed.

## Device/firmware anchor

All values below came from Gate 0 ADB evidence.

| Item | Exact observed value |
|---|---|
| Device model | `SM-G9810` |
| Device codename | `x1q` |
| Build display ID | `TP1A.220624.014.G9810ZCSBHXJ2` |
| Incremental build | `G9810ZCSBHXJ2` |
| Bootloader | `G9810ZCSBHXJ2` |
| Bootloader revision token | `B` (recorded as the raw revision character; no numeric conversion asserted) |
| Security patch | `2024-09-01` |
| Kernel | `Linux localhost 4.19.113-964403 #1 SMP PREEMPT Tue Oct 15 12:52:48 KST 2024 aarch64 Toybox` |
| Stock config machine selector | `CONFIG_MACH_X1Q_CHN_OPEN=y` |

Samsung's firmware history independently lists `G9810ZCSBHXJ2` for SM-G9810,
Android 13, release date 2024-10-28, and security patch 2024-09-01:

- https://doc.samsungmobile.com/SM-G9810/011974200319/eng.html

## Samsung Open Source Release Center results

### Exact firmware query

Query:

- https://opensource.samsung.com/uploadSearch?searchValue=G9810ZCSBHXJ2

Observed result on 2026-08-23:

```text
This is the result of your ‘G9810ZCSBHXJ2’. 0 of results found.
Result : 0
No results has been uploaded in this category.
```

### Exact model query

Query:

- https://opensource.samsung.com/uploadSearch?searchValue=SM-G9810

The only result was:

| OSRC field | Value |
|---|---|
| Model | `SM-G9810` |
| Version | `G9810ZHU6HWH9` |
| Description/package | `SM-G9810_HK_13_Opensource.zip` |
| OSRC upload identifier | `11969` |

This is not the phone's firmware. It is an HK release with revision token `6`,
whereas the device is on the China-open `G9810ZCSBHXJ2` release with revision
token `B`.

### Same build suffix on a sibling model

Query:

- https://opensource.samsung.com/uploadSearch?searchValue=G9860ZCSBHXJ2

The result was:

| OSRC field | Value |
|---|---|
| Model | `SM-G9860` |
| Version | `G9860ZCSBHXJ2` |
| Description/package | `SM-G9860_CHN_13_Opensource.zip` |
| OSRC upload identifier | `12985` |

The suffix, Android generation, security-patch generation, and chipset family
make this useful investigative evidence, but the model is `SM-G9860`, not
`SM-G9810`. It cannot be promoted to the exact source package without evidence
inside Samsung's archive showing that its kernel drop and x1q China-open
defconfig are shared with `SM-G9810`.

## Source package record

| Item | Result |
|---|---|
| Exact Samsung source package | **Not identified** |
| Exact release identifier/URL | OSRC exact-firmware query returns zero results |
| Exact source package SHA256 | Not available; no exact package exists in the observed OSRC results and no archive was downloaded |
| Exact kernel source version | Not verified from a matching Samsung archive |
| Exact Samsung build README path | Not verified |
| Exact SM-G9810/x1q defconfig path | **Not verified** |
| Exact Samsung GCC toolchain version | Not verified |
| Exact Samsung build output path | Not verified from a matching archive |

## Direct source inspection (secondary evidence only)

Because the exact Samsung archive could not be selected, the following modified
third-party x1q tree was inspected only to understand naming and build metadata:

- Repository: https://github.com/xwenx90/GalaxyS20_Series_KernelSU_Next_Susfs
- Commit: `882a4b75dffcf400aa4dbb3fcf739d988c1a64e0`
- Declared region: Korea
- Declared base: Android 13 / One UI 5.1 / Linux 4.19.113
- Known modifications: KernelSU Next, SUSFS, and disabled Samsung security
  features

Files actually read:

```text
README.md
build_kernel.sh
Makefile
arch/arm64/configs/vendor/x1q_kor_singlex_defconfig
```

The tree contains no model/build identifier tying it to `SM-G9810` or
`G9810ZCSBHXJ2`. Its only checked-in x1q defconfig path is:

```text
arch/arm64/configs/vendor/x1q_kor_singlex_defconfig
```

That path is definitively wrong for the connected phone because:

```text
stock:     CONFIG_MACH_X1Q_CHN_OPEN=y
candidate: # CONFIG_MACH_X1Q_CHN_OPEN is not set
candidate: CONFIG_MACH_X1Q_KOR_SINGLE=y
```

The likely spelling `arch/arm64/configs/vendor/x1q_chn_open_defconfig` is only an
inference from Samsung's symbol naming. It is deliberately **not** recorded as
the exact defconfig until observed inside a suitable Samsung package.

## Key stock-vs-auxiliary-defconfig differences

A direct text-level Kconfig comparison found 5,805 symbols in the captured stock
config and 5,780 in the auxiliary defconfig: 12 common symbols had different
values, 41 appeared only in stock, and 16 only in the auxiliary config.

Important differences include:

| Symbol | Stock phone | Auxiliary Korean tree |
|---|---|---|
| `CONFIG_MACH_X1Q_CHN_OPEN` | `y` | not set |
| `CONFIG_MACH_X1Q_KOR_SINGLE` | not set | `y` |
| `CONFIG_WLAN_REGION_CODE` | `300` | `200` |
| `CONFIG_UH` | `y` | not set |
| `CONFIG_CFP` | `y` | not set |
| `CONFIG_PROCA` | `y` | not set |
| `CONFIG_SECURITY_DEFEX` | `y` | not set |
| `CONFIG_FIVE` | `y` | not set |
| `CONFIG_KSU` | absent | `y` |
| `CONFIG_KSU_SUSFS` | absent | `y` |

The namespace-related values happen to agree, but this does not cure the region,
security, or provenance mismatch:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
# CONFIG_USER_NS is not set
# CONFIG_PID_NS is not set
CONFIG_NET_NS=y
# CONFIG_VETH is not set
```

Neither config contains a `CONFIG_IPC_NS` line because `CONFIG_SYSVIPC` is not
enabled.

## Toolchain metadata

### Directly observed from the stock config

```text
Compiler: clang version 10.0.6 for Android NDK
CONFIG_GCC_VERSION=0
CONFIG_CC_IS_CLANG=y
CONFIG_CLANG_VERSION=100006
```

This confirms the compiler family/version used for the running kernel, but not
the exact Samsung toolchain archive or GCC cross-toolchain patch release.

### Auxiliary build script metadata

The inspected `build_kernel.sh` uses:

```text
ARCH=arm64
CROSS_COMPILE=toolchain/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-
REAL_CC=toolchain/llvm-arm-toolchain-ship/10.0/bin/clang
CLANG_TRIPLE=aarch64-linux-gnu-
DTC_EXT=tools/dtc
CONFIG_BUILD_ARM64_DT_OVERLAY=y
O=out
candidate output=out/arch/arm64/boot/Image
```

The auxiliary Makefile declares `VERSION=4`, `PATCHLEVEL=19`, and
`SUBLEVEL=113`. These values corroborate the broad kernel lineage, not the exact
firmware/source match. The GCC 4.9 path and the above build variables remain
secondary evidence until confirmed in the matching Samsung README/build script.

## Proposed stock-baseline command (do not execute)

There is intentionally no executable Gate 2 command yet. After an exact Samsung
package and defconfig are verified, the candidate recipe has the following
shape:

```sh
# DO NOT RUN while Gate 1 is BLOCKED.
make -j"$(nproc)" -C "$KERNEL_SRC" O="$OUT" \
  DTC_EXT="$KERNEL_SRC/tools/dtc" CONFIG_BUILD_ARM64_DT_OVERLAY=y \
  ARCH=arm64 \
  CROSS_COMPILE="$KERNEL_SRC/toolchain/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-" \
  REAL_CC="$KERNEL_SRC/toolchain/llvm-arm-toolchain-ship/10.0/bin/clang" \
  CLANG_TRIPLE=aarch64-linux-gnu- \
  '<VERIFIED_SM-G9810_CHN_DEFCONFIG>'

make -j"$(nproc)" -C "$KERNEL_SRC" O="$OUT" \
  DTC_EXT="$KERNEL_SRC/tools/dtc" CONFIG_BUILD_ARM64_DT_OVERLAY=y \
  ARCH=arm64 \
  CROSS_COMPILE="$KERNEL_SRC/toolchain/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-" \
  REAL_CC="$KERNEL_SRC/toolchain/llvm-arm-toolchain-ship/10.0/bin/clang" \
  CLANG_TRIPLE=aarch64-linux-gnu-
```

The placeholder is intentional. Substituting the Korean defconfig would violate
Gate 1.

## DroidSpaces reference boundary

DroidSpaces documents Linux 4.19 as a non-GKI/legacy kernel and requires PID and
IPC namespaces for container startup. That requirement explains the future
configuration goal but provides no evidence that a Samsung source package
matches this firmware:

- https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/Kernel-Configuration.md
- https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/community-supported-devices.md

The community-supported-device list does not identify SM-G9810/x1q as a verified
device.

## Required evidence to unblock Gate 1

One of the following must be obtained and reviewed before Gate 2:

1. a Samsung OSRC package explicitly released for `SM-G9810` and
   `G9810ZCSBHXJ2`; or
2. authoritative Samsung package contents/documentation proving that
   `SM-G9860_CHN_13_Opensource.zip` is the shared kernel drop for the
   `SM-G9810` China-open firmware, including an x1q China-open defconfig.

The selected archive must then be checksummed and its `README*`, `build*.sh`,
top-level `Makefile`, `arch/arm64/configs/*`, and related vendor config files must
be read before changing this status.
