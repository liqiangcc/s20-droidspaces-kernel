# Verification Commands

## Device baseline

```sh
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.build.display.id
adb shell getprop ro.build.version.incremental
adb shell getprop ro.bootloader
adb shell uname -a
adb shell su -c 'zcat /proc/config.gz' > stock.config
```

## Kernel config

```sh
scripts/verify-stock-config.sh stock.config
scripts/verify-droidspaces-config.sh out/.config
```

## DroidSpaces runtime (post-flash only)

```sh
adb shell su -c '/data/local/Droidspaces/bin/droidspaces check'
```

These commands verify state only; none writes a device partition.
