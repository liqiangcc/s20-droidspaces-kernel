# Samsung Source Archive Comparison Evidence

Captured/reviewed: 2026-08-23 (Asia/Shanghai)

## Scope and result

Three original Samsung `Kernel.tar.gz` archives were compared entry by entry.
No kernel configuration or compilation command was run.

```text
Gate 1 = BLOCKED
```

The comparison establishes a strong reconstructed-source recipe but does not
prove that Samsung released the exact SM-G9810 China-open HXJ2 source.

## Input archives

| Role | Outer package | SHA256 |
|---|---|---|
| Old official x1q China/HK | `SM-G9810_HK_13_Opensource.zip` | `9c3d5249a687d93c68290fb0b2ec3b4b2069fd6c224d8cd49ce46b217e828ea8` |
| Current-generation official x1q KOR | `SM-G981N_KOR_13_Opensource.zip` | `4deff23b76547dfa8d7f0ae8e0579d329e2851b2781bbe7a7be521830aa51884` |
| Exact-suffix official y2q China | `SM-G9860_CHN_13_Opensource.zip` | `d3595efa1f00a60768958b1fbc95703c954cb3997f11b1ca66ef318a7734c87c` |

The KOR archive was downloaded from the OSRC `G981NKSS6IXJ1` result. Its outer
filename does not encode the version; its 2024-10-14 source timestamps
corroborate that selection and are one day before the connected phone's
2024-10-15 stock-kernel build.

## Comparison method

Windows cannot materialize every Linux symlink and reserved filename in these
archives. Therefore the authoritative comparison streamed the original tar
archives directly:

```text
python scripts/compare-source-archives.py KOR/Kernel.tar.gz CHN/Kernel.tar.gz
python scripts/compare-source-archives.py KOR/Kernel.tar.gz HK/Kernel.tar.gz
python scripts/compare-source-archives.py KOR/Kernel.tar.gz HK/Kernel.tar.gz \
  --third CHN/Kernel.tar.gz
```

For every regular file, the script records size and SHA256. Symlink and hardlink
entries are compared by type and link target.

## KOR IXJ1 x1q versus CHN HXJ2 y2q

```text
KOR entries=70947
CHN entries=70958
common entries=70943
identical common entries=70935
changed common entries=8
KOR-only entries=4
CHN-only entries=15
```

The four KOR-only entries are its x1q KOR defconfig and x1q DTS files. Nine of
the CHN-only entries are the y2q China defconfig/DTS files; six are an
`mt7621-mmc` staging directory present only in that package.

The eight changed common files are:

```text
arch/arm64/Kconfig.projects
arch/arm64/boot/dts/samsung/Makefile
build_kernel.sh
drivers/gpu/drm/drm_edid.c
drivers/usb/gadget/function/f_ss_mon_gadget.c
include/linux/ologk.h
techpack/display/msm/dp/dp_display.c
techpack/display/msm/dp/secdp.h
```

The first three select x1q KOR versus y2q China. The five runtime differences
move an HDR capability check, add/remove a USB GUID-length guard, change an olog
header include, and place the DisplayPort HDR helper declaration differently.

## KOR IXJ1 x1q versus HK HWH9 x1q

```text
KOR entries=70947
HK entries=70951
common entries=70944
identical common entries=70900
changed common entries=44
KOR-only entries=3
HK-only entries=7
```

KOR-only entries are its KOR defconfig and r13/r14 KOR overlays. HK-only entries
are its China/HK defconfig and six x1q China overlays (r07, r08, r09, r12, r13,
r14).

## Three-way provenance classification

Using KOR as left, HK as right, and CHN as third:

```text
all three byte-identical=70898
KOR and CHN same, HK different/absent=44
HK and CHN same, KOR different/absent=8
KOR and HK same, CHN different/absent=17
all three different=2
```

The `KOR and CHN same` group consists of 37 newer common-source files plus seven
x1q China files absent from both non-HK packages. The 37 common files cover MHI,
ADSP RPC, GPU/IOMMU, NPU, USB, memory management, networking, SDP security, and
audio. This strongly identifies the KOR package as the same broad 2024 source
generation as CHN HXJ2.

The `HK and CHN same` group contains three KOR-only device files plus these five
actual common regional differences:

```text
drivers/gpu/drm/drm_edid.c
drivers/usb/gadget/function/f_ss_mon_gadget.c
include/linux/ologk.h
techpack/display/msm/dp/dp_display.c
techpack/display/msm/dp/secdp.h
```

The two all-different files are:

```text
arch/arm64/Kconfig.projects
build_kernel.sh
```

## Stock Kconfig coverage

Static parsing of every KOR `Kconfig*` file found:

```text
Kconfig definition matches=19316
unique defined symbols before HK project Kconfig=18276
stock.config symbols=5805
stock symbols without a direct KOR definition=17
enabled missing symbols=1: CONFIG_MACH_X1Q_CHN_OPEN
```

Adding the official HK `arch/arm64/Kconfig.projects` definitions changes the
result to:

```text
enabled missing symbols=0
remaining missing symbols=15
```

All 15 remaining symbols are explicit `not set` selectors for unrelated Samsung
models/regions. The source also directly defines `PID_NS`, `IPC_NS`, `USER_NS`,
and `VETH`; `IPC_NS` depends on `SYSVIPC || POSIX_MQUEUE`.

## x1q DTS comparison

Direct KOR-to-HK comparisons for both r13 and r14 overlays produced:

```text
added lines=2
removed lines=6
```

The r14 changes are limited to:

```text
KOR versus CHN model string
one regulator-always-on property
SX9360 proximity sensor threshold/filter properties
```

This is strong device-family continuity evidence, but it does not prove that
the 2023 HK x1q China DTS is byte-identical to the unavailable 2024 China DTS.

## Candidate boundary

A traceable experimental source candidate could be assembled from:

```text
1. SM-G981N KOR IXJ1 as the current-generation x1q base;
2. the five China-common runtime files corroborated by both HK and CHN packages;
3. x1q China project Kconfig and DTS provenance from the official HK package;
4. evidence/stock.config as the configuration anchor.
```

This candidate was not assembled or compiled during this gate. Its China x1q
DTS provenance remains older than the phone firmware, so it cannot be labeled
an exact Samsung stock source release.

## Reconstructed candidate artifact

The owner subsequently instructed the experimental reconstruction route to
continue. The candidate was assembled without configuring or compiling the
kernel:

```text
path: D:\codex-source-analysis\s20-20260823\candidate\SM-G9810_X1Q_CHN_HXJ2_RECONSTRUCTED_Kernel.tar.gz
size: 212189708 bytes
SHA256: a66cae75d49016be8e3129329ef0d265409546901ff11ab58fd984bf6db51fa5
entries: 70952
```

Reproduction tool:

```text
scripts/assemble-source-candidate.py
```

Independent candidate-vs-KOR archive comparison:

```text
common entries=70944
identical common entries=70938
changed common entries=6
only KOR=3
only candidate=8
unexpected differences=0
```

The six replacements are exactly:

```text
arch/arm64/Kconfig.projects
drivers/gpu/drm/drm_edid.c
drivers/usb/gadget/function/f_ss_mon_gadget.c
include/linux/ologk.h
techpack/display/msm/dp/dp_display.c
techpack/display/msm/dp/secdp.h
```

The three removed entries are the KOR defconfig and r13/r14 KOR overlays. The
eight additions are the HK x1q China defconfig, six China overlays, and the
embedded provenance document.

Static candidate coverage command/result:

```text
python scripts/check-kconfig-coverage.py <candidate.tar.gz> evidence/stock.config

defined symbols=18277
stock config symbols=5805
missing symbols=16
active missing symbols=0
```

The 16 missing symbols are all explicitly disabled selectors for other Samsung
regions/models. The artifact's `CANDIDATE_PROVENANCE.md` also warns that the
inherited KOR `build_kernel.sh` names a removed KOR defconfig and must not be
executed.

No `make`, compiler, kernel build, boot image, or flashing command was executed.
