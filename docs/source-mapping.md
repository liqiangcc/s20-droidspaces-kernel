# Source Mapping

## Objective

Identify the exact Samsung kernel source package and device defconfig that correspond to the phone's current SM-G9810 firmware before compiling anything.

## Authoritative source first

Primary source:

- Samsung Open Source Release Center: https://opensource.samsung.com/

Search for `SM-G9810` and match the source release to the exact values recorded in `docs/device-baseline.md`.

Do not select a source package only because it is:

- Galaxy S20;
- `x1q`;
- Linux 4.19.113;
- Android 13 / One UI 5.1.

Those properties are necessary but not sufficient for a safe match.

## Required mapping record

Before Gate 1 is complete, fill this table:

| Item | Exact value |
|---|---|
| Device model | SM-G9810 |
| Device codename | x1q |
| Current build display ID | TODO |
| Current incremental build | TODO |
| Current bootloader revision | TODO |
| Current `uname -a` | TODO |
| Samsung source package | TODO |
| Samsung source release URL / identifier | TODO |
| Kernel source version | TODO |
| Build README path | TODO |
| Device defconfig path | TODO |
| Required toolchain version(s) | TODO |

## Third-party references

Third-party `x1q` projects may be used to learn how Snapdragon S20 kernels are built and packaged, but they are **secondary evidence only**.

For every third-party reference, record:

- exact supported model(s);
- region (`CHC`, `KOR`, etc.);
- Android/One UI version;
- kernel base/version;
- defconfig used;
- security features changed;
- ramdisk/DTB/DTBO/package changes;
- whether any binary artifact is being reused (default: no).

A reference implementation must never silently become the source of truth for SM-G9810.

## DroidSpaces references

Use these only after the Samsung source/defconfig mapping is complete:

- Kernel configuration: https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/Kernel-Configuration.md
- Community-supported devices: https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/community-supported-devices.md

The community-device document is a pattern for adaptation and validation, not a source of cross-device flashable kernels.
