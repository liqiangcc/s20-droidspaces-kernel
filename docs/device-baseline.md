# Device Baseline

## Gate 0 status

Gate 0 device/firmware baseline capture completed from the USB-connected phone
on 2026-08-23 (Asia/Shanghai). The device serial is deliberately not recorded.

The preconditions were observed directly:

```text
adb state=device
su uid=0(root) gid=0(root) groups=0(root) context=u:r:magisk:s0
```

## Exact observed device and firmware values

| ADB source | Exact raw value |
|---|---|
| `ro.product.model` | `SM-G9810` |
| `ro.product.device` | `x1q` |
| `ro.build.display.id` | `TP1A.220624.014.G9810ZCSBHXJ2` |
| `ro.build.version.incremental` | `G9810ZCSBHXJ2` |
| `ro.bootloader` | `G9810ZCSBHXJ2` |
| `ro.build.version.security_patch` | `2024-09-01` |
| `uname -a` | `Linux localhost 4.19.113-964403 #1 SMP PREEMPT Tue Oct 15 12:52:48 KST 2024 aarch64 Toybox` |

The complete command transcript is preserved in
`evidence/device-properties.txt`.

## Stock kernel configuration evidence

The complete decompressed `/proc/config.gz` is preserved as
`evidence/stock.config`.

```text
SHA256: 6c2ca2e167be843a246d483ea591527e7eec13a21f05dad6fb82a5d09afcbdaf
Size: 197847 bytes
Generated header: Linux/arm64 4.19.113 Kernel Configuration
```

The exact requested grep produced:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
# CONFIG_USER_NS is not set
# CONFIG_PID_NS is not set
CONFIG_NET_NS=y
# CONFIG_NET_NSH is not set
# CONFIG_VETH is not set
```

`CONFIG_NET_NSH` appears because the requested expression is not end-anchored.
There is no `CONFIG_IPC_NS` line in the captured config; this is recorded as
absence rather than rewritten as a synthetic `# CONFIG_IPC_NS is not set` line.

## Gate boundary

No boot image was read, unpacked, generated, or written during Gate 0. No
kernel build command was executed.
