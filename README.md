# s20-droidspaces-kernel

Kernel adaptation workspace for running DroidSpaces on the Samsung Galaxy S20 5G (SM-G9810 / x1q / Snapdragon 865) while keeping the scope as small and auditable as possible.

## Current device baseline

- Device: Samsung Galaxy S20 5G
- Model: SM-G9810
- Codename: x1q
- SoC: Qualcomm Snapdragon 865 (SM8250)
- Android: One UI 5.1 / Android 13
- Kernel: Samsung 4.19.113 lineage
- Root: Magisk

## Confirmed blocker

The stock kernel exposes namespace support in general but has the following relevant configuration disabled:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
# CONFIG_PID_NS is not set
# CONFIG_IPC_NS is not set
# CONFIG_USER_NS is not set
# CONFIG_VETH is not set
```

DroidSpaces refuses to start because PID and IPC namespaces are required. `USER_NS` and `VETH` are also desirable for nested container workloads and NAT networking.

## Goal

Produce a reproducible, minimally modified kernel build that:

1. boots the existing SM-G9810 firmware without changing userdata;
2. preserves the stock boot ramdisk, command line, DTB/DTBO handling, and vendor integration unless a change is proven necessary;
3. enables the DroidSpaces-required kernel capabilities;
4. is tested through explicit gates before any real-device flash;
5. always has a documented rollback path to the original boot image.

## Safety rule

This repository must not treat a successfully compiled kernel as flash-ready. The first build target is a **stock-baseline kernel with zero DroidSpaces changes**. Only after that build and boot path is validated should the DroidSpaces configuration fragment be applied.

See `docs/test-plan.md` for the validation gates and `docs/recovery.md` for rollback requirements.
