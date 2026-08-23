# Device Baseline

## Confirmed device identity

| Field | Value | Status |
|---|---|---|
| Product | Samsung Galaxy S20 5G | confirmed |
| Model | SM-G9810 | confirmed |
| Codename | x1q | confirmed |
| SoC | Qualcomm Snapdragon 865 / SM8250 | confirmed |
| Android | Android 13 / One UI 5.1 | confirmed |
| Kernel lineage | Linux 4.19.113 | confirmed |
| Root | Magisk | confirmed |

## Exact firmware values still required

Before any source package is selected or any kernel is compiled, capture these directly from the phone:

```sh
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.build.display.id
adb shell getprop ro.build.version.incremental
adb shell getprop ro.bootloader
adb shell uname -a
```

Record the output below before Gate 1:

```text
ro.product.model=
ro.product.device=
ro.build.display.id=
ro.build.version.incremental=
ro.bootloader=
uname -a=
```

## Stock kernel configuration evidence

The current stock kernel has been observed with the following namespace/network configuration:

```text
CONFIG_NAMESPACES=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
# CONFIG_IPC_NS is not set
# CONFIG_PID_NS is not set
# CONFIG_USER_NS is not set
# CONFIG_VETH is not set
```

The full stock config should be captured and committed as an evidence artifact before building:

```sh
adb shell su -c 'zcat /proc/config.gz' > stock.config
sha256sum stock.config
```

Do not replace the observed stock config with the defconfig from a third-party `x1q` kernel.
