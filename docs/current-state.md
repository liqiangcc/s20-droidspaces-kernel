# Current State

## What is proven

- Device is Galaxy S20 5G SM-G9810 (`x1q`), Snapdragon 865.
- Android is One UI 5.1 / Android 13.
- Kernel lineage is 4.19.113.
- Magisk root is functional.
- DroidSpaces itself can obtain root and run its requirement checker.
- DroidSpaces refuses to start because PID and IPC namespaces are missing.
- `/proc/config.gz` confirms `PID_NS` and `IPC_NS` are not built into the stock kernel.
- `USER_NS` and `VETH` are also disabled.

## What is not yet proven

- exact firmware/build/source package mapping;
- exact Samsung defconfig path for this firmware;
- authoritative Samsung toolchain for this source package;
- ability to reproduce the stock kernel from source;
- exact boot-image repack workflow for this firmware;
- whether enabling the DroidSpaces requirements introduces any Samsung vendor regressions.

## Next milestone

Complete Gate 0 and Gate 1 from `docs/work-handoff.md`.

No kernel compilation or flashing should begin until the exact firmware-to-source mapping is reviewed.
