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

### Direct inspection of the official SM-G9860 package

The official sibling package was subsequently downloaded and fully read without
ZIP errors:

| Item | Observed value |
|---|---|
| Package | `SM-G9860_CHN_13_Opensource.zip` |
| OSRC version | `G9860ZCSBHXJ2` |
| OSRC upload identifier | `12985` |
| File size | `254544062` bytes |
| SHA256 | `d3595efa1f00a60768958b1fbc95703c954cb3997f11b1ca66ef318a7734c87c` |
| Kernel README | top-level `README_Kernel.txt` |
| Kernel archive | top-level `Kernel.tar.gz` |
| Kernel version | `4.19.113` |
| Defconfig | `arch/arm64/configs/vendor/y2q_chn_openx_defconfig` |
| Output | `arch/arm64/boot/Image` |

The kernel archive contains 76,067 paths, zero of which contain `x1q`. Its only
vendor defconfig is `y2q_chn_openx_defconfig`, and its Samsung DTS directory is
`arch/arm64/boot/dts/samsung/y2q`. The README build command also explicitly
selects `vendor/y2q_chn_openx_defconfig`.

The decisive machine-selector difference is:

```text
stock SM-G9810: CONFIG_MACH_X1Q_CHN_OPEN=y
G9860 package:  CONFIG_MACH_Y2Q_CHN_OPEN=y
```

Consequently, direct package inspection disproves the hypothesis that this
archive includes the missing SM-G9810/x1q China-open defconfig. It remains
useful for same-release toolchain corroboration but cannot unblock Gate 1.

### Direct inspection of the official SM-G981N x1q package

The OSRC package selected from the `G981NKSS6IXJ1` result was downloaded and
fully read without ZIP errors. The outer filename does not embed the release
identifier, so the association with `G981NKSS6IXJ1` comes from the selected
OSRC result; the archive's 2024-10-14 timestamps independently corroborate that
generation. This is one day before the phone's 2024-10-15 stock-kernel build.

| Item | Observed value |
|---|---|
| Package | `SM-G981N_KOR_13_Opensource.zip` |
| Selected OSRC version | `G981NKSS6IXJ1` |
| File size | `253046595` bytes |
| SHA256 | `4deff23b76547dfa8d7f0ae8e0579d329e2851b2781bbe7a7be521830aa51884` |
| ZIP full-read result | OK; 4 entries, 255914793 uncompressed bytes |
| Kernel README | top-level `README_Kernel.txt` |
| Kernel version | `4.19.113` |
| Defconfig | `arch/arm64/configs/vendor/x1q_kor_singlex_defconfig` |
| x1q DTS | `arch/arm64/boot/dts/samsung/x1q/` |
| Output | `arch/arm64/boot/Image` |

The KOR defconfig is structurally very close to the captured stock config:

```text
stock symbols=5805
KOR symbols=5809
changed common symbols=5
stock-only symbols=10 (all explicit disabled SEC project selectors)
KOR-only symbols=14 (MPTCP detail plus MST/MFC charger selections)
```

The five common-symbol differences are:

```text
CONFIG_MACH_X1Q_CHN_OPEN: stock=y; KOR=not set
CONFIG_MACH_X1Q_KOR_SINGLE: stock=not set; KOR=y
CONFIG_MPTCP: stock=not set; KOR=y
CONFIG_SUPPORT_MCC_THRESHOLD_CHANGE: stock=not set; KOR=y
CONFIG_WLAN_REGION_CODE: stock=300; KOR=200
```

To test whether this is the same broad source generation as the exact-suffix
SM-G9860 package, SHA256 hashes were compared for selected critical common
files. All seven were byte-identical between the KOR x1q and CHN y2q packages:

```text
Makefile
kernel/fork.c
kernel/nsproxy.c
ipc/namespace.c
net/core/net_namespace.c
drivers/android/binder.c
security/selinux/hooks.c
```

This makes the SM-G981N package the strongest available first-party x1q source
candidate. It still does not establish an exact firmware/region match: its
README and defconfig select Korea, while the phone selects x1q China-open.

### Full three-package convergence analysis

The three original `Kernel.tar.gz` archives were compared without extraction
using `scripts/compare-source-archives.py`. The script hashes every regular
file and compares link metadata, avoiding Windows path and symlink limitations.
Full command results and path classifications are recorded in
`evidence/source-archive-comparison.md`.

| Comparison | Common entries | Byte-identical | Changed common | Only first | Only second |
|---|---:|---:|---:|---:|---:|
| KOR IXJ1 x1q vs CHN HXJ2 y2q | 70,943 | 70,935 | 8 | 4 | 15 |
| KOR IXJ1 x1q vs HK HWH9 x1q | 70,944 | 70,900 | 44 | 3 | 7 |

Of the eight KOR-vs-CHN common-file differences, three are expected project,
DTS-directory, and build-script selectors. The remaining five are small
regional implementation differences in DisplayPort/HDR, Samsung USB monitoring,
and olog headers. The namespace, IPC, Binder, and SELinux sources are identical.

Three-way classification found 70,898 entries identical in all packages. After
excluding files absent because of device packaging:

- 37 common files use the same newer content in KOR IXJ1 and CHN HXJ2 but older
  content in HK HWH9; this is strong evidence of a shared 2024 source generation;
- five common runtime files use the same China-region content in HK HWH9 and
  CHN HXJ2 but different KOR content;
- the x1q China DTS and defconfig exist only in the older HK archive;
- `arch/arm64/Kconfig.projects` and `build_kernel.sh` differ in all three and
  must be selected for the target project rather than copied blindly.

Static Kconfig parsing found 18,276 symbols defined by the KOR tree. Of the
5,805 symbols in `stock.config`, 17 lacked a direct definition in that regional
tree, but only one was enabled: `CONFIG_MACH_X1Q_CHN_OPEN=y`. Replacing the KOR
project Kconfig with Samsung's HK x1q China project Kconfig resolves every
enabled stock symbol. The 15 remaining unmatched symbols are all disabled
selectors for other Samsung projects.

The KOR and HK x1q r13/r14 DTS overlays are also close: each comparison has two
added and six removed lines, covering the regional model string, one regulator
flag, and proximity-sensor thresholds. This is useful provenance, not proof
that the 2023 HK DTS is the exact 2024 China-open DTS.

These results establish a defensible **reconstructed experimental candidate**:

```text
base: current-generation SM-G981N KOR x1q source
generation updates: corroborated by SM-G9860 CHN HXJ2
China regional common files: versions shared by HK x1q and CHN HXJ2
x1q China project Kconfig/DTS provenance: official SM-G9810 HK archive
configuration anchor: captured stock.config
```

No candidate tree was assembled and no build was run. This triangulation does
not turn the reconstructed candidate into an exact Samsung release, so Gate 1
remains blocked under the repository's exact-match rule.

## Source package record

| Item | Result |
|---|---|
| Exact Samsung source package | **Not identified** |
| Exact release identifier/URL | OSRC exact-firmware query returns zero results |
| Exact source package SHA256 | Not available; the downloaded sibling package SHA256 is `d3595efa1f00a60768958b1fbc95703c954cb3997f11b1ca66ef318a7734c87c` but it is not the exact model |
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

### Official same-release sibling package

`README_Kernel.txt` and the top-level `Makefile` in Samsung's downloaded
SM-G9860 package directly specify/corroborate:

```text
ARCH=arm64
CROSS_COMPILE=<android platform>/prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9/bin/aarch64-linux-android-
REAL_CC=toolchain/llvm-arm-toolchain-ship/10.0/bin/clang
CLANG_TRIPLE=aarch64-linux-gnu-
DTC_EXT=tools/dtc
CONFIG_BUILD_ARM64_DT_OVERLAY=y
O=out
output=arch/arm64/boot/Image
```

This is first-party evidence for the `G9860ZCSBHXJ2` sibling release and agrees
with the running kernel's Clang 10.0.6 metadata. It still does not prove that
the unavailable SM-G9810 release used an identical toolchain archive/revision.

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

Before Gate 2, a Samsung OSRC package explicitly released for `SM-G9810` and
`G9810ZCSBHXJ2`, or another authoritative Samsung package that actually
contains the matching x1q China-open source and defconfig, must be obtained and
reviewed. The inspected `SM-G9860_CHN_13_Opensource.zip` cannot satisfy this
condition because it contains only y2q device paths and configuration. The
inspected SM-G981N package supplies current-generation x1q source but only a
Korean defconfig, so it narrows the uncertainty without removing it.

The selected archive must then be checksummed and its `README*`, `build*.sh`,
top-level `Makefile`, `arch/arm64/configs/*`, and related vendor config files must
be read before changing this status.
