# Codex Work Handoff

## Immediate next task

Complete **Gate 0 and Gate 1 only**. Do not compile yet.

### Gate 0 — capture the exact device baseline

Collect from the real phone:

```sh
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.build.display.id
adb shell getprop ro.build.version.incremental
adb shell getprop ro.bootloader
adb shell uname -a
adb shell su -c 'zcat /proc/config.gz' > stock.config
sha256sum stock.config
```

Update `docs/device-baseline.md` with the exact outputs and preserve `stock.config` as evidence if it is safe to commit.

### Gate 1 — source mapping

Using the exact device/firmware values:

1. locate the matching SM-G9810 release in Samsung Open Source Release Center;
2. download/checksum the source archive;
3. identify the kernel build README;
4. identify the exact device defconfig;
5. identify the toolchain required by Samsung's build instructions;
6. update `docs/source-mapping.md` with evidence and exact identifiers.

Do not substitute a Korean `x1q` defconfig or a third-party KernelSU kernel unless it is used only as a documented secondary reference.

## Stop condition

After Gate 0 and Gate 1 are complete, stop and report:

- exact firmware/source match;
- defconfig path;
- toolchain versions;
- unresolved risks/mismatches;
- exact proposed stock-baseline build command.

Do **not** start Gate 2 until the source mapping is reviewed.
