# Decision Log

## 2026-08-23 — Treat stock kernel capability gap as the primary blocker

Observed on SM-G9810 stock kernel:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
# CONFIG_PID_NS is not set
# CONFIG_IPC_NS is not set
# CONFIG_USER_NS is not set
# CONFIG_VETH is not set
```

DroidSpaces runtime check independently reported missing PID and IPC namespace support and refused to start a container.

Decision: stop changing DroidSpaces versions/rootfs/storage/network settings. Move the investigation to a stock-source kernel adaptation.

## 2026-08-23 — Do not use a broad third-party kernel as the first flash candidate

Third-party Snapdragon S20 kernels are useful as references for source layout, toolchains, packaging, and device quirks, but often bundle KernelSU/SUSFS/security-feature removals/performance changes.

Decision: first produce a stock-baseline rebuild from the exact Samsung source/defconfig, then apply a minimal DroidSpaces delta.

## 2026-08-23 — Flashing remains a manual gate

Agents may research, build, compare, package, and prepare rollback artifacts.

Decision: no automated flashing. A human must review source mapping, config diff, boot-image diff, checksums, and recovery path before the first device write.
