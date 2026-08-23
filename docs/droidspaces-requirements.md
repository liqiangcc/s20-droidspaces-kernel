# DroidSpaces Requirements Gap

## Runtime evidence

DroidSpaces currently refuses to start a container because the stock kernel lacks two mandatory namespace features:

```text
PID namespace is not supported by the kernel
IPC namespace is not supported by the kernel
Missing 2 required feature(s) - cannot proceed
```

The runtime check and `/proc/config.gz` evidence agree: this is a kernel capability gap, not a rootfs, storage-size, Magisk permission, daemon-mode, or DroidSpaces version issue.

## Current relevant stock config

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
# CONFIG_PID_NS is not set
# CONFIG_IPC_NS is not set
# CONFIG_USER_NS is not set
# CONFIG_VETH is not set
```

## Minimal mandatory target

The first DroidSpaces-capable kernel must at least produce:

```text
CONFIG_NAMESPACES=y
CONFIG_PID_NS=y
CONFIG_IPC_NS=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
```

## Extended target

For the intended long-term use (container networking and possible nested Docker/Podman), also evaluate and preferably enable:

```text
CONFIG_USER_NS=y
CONFIG_VETH=y
```

These are **not** a substitute for checking the complete DroidSpaces non-GKI kernel requirements. Before the modified build is accepted, compare the final `.config` against the current DroidSpaces 4.19/non-GKI documentation.

Reference:

- https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/Kernel-Configuration.md
- https://github.com/ravindu644/Droidspaces-OSS/blob/main/Documentation/community-supported-devices.md

## Scope control

Do not solve these missing options by importing a broad third-party kernel feature set. In particular, do not combine this change with:

- KernelSU/SUSFS integration;
- disabling Samsung RKP/KDP/DEFEX/PROCA/CFP unless proven strictly necessary;
- scheduler/performance tuning;
- DTB/DTBO changes unrelated to the namespace options;
- custom SELinux policy unrelated to DroidSpaces requirements.
