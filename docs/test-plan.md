# Test Plan

The project uses explicit gates. A later gate must not be started when an earlier gate is unresolved.

## Gate 0 — Recovery baseline

Before flashing any experimental image:

- exact device/firmware identity captured;
- current working boot image backed up;
- `boot-stock.img` SHA256 recorded;
- current `stock.config` captured;
- a tested path exists to enter Samsung Download Mode / recovery and restore the stock boot image.

## Gate 1 — Source mapping

Pass when:

- matching Samsung source package is identified;
- exact defconfig is identified;
- build instructions/toolchain are documented;
- no unresolved region/model mismatch remains.

## Gate 2 — Stock baseline compile

Compile with no DroidSpaces changes.

Pass when:

- build succeeds reproducibly;
- config diff versus captured stock config is reviewed;
- build artifact/checksums are recorded.

## Gate 3 — Stock baseline packaging

Prepare a boot image with the rebuilt stock-baseline kernel while preserving existing boot metadata/ramdisk as far as the actual device format permits.

Pass when static inspection shows only intended differences.

**Manual flash approval is required before device testing.**

## Gate 4 — Stock baseline device smoke test

After manual flash:

```text
Android boots
ADB works
Wi-Fi works
USB works
Magisk/root works
no reboot loop / kernel panic pattern
```

Also capture:

```sh
adb shell uname -a
adb shell su -c 'zcat /proc/config.gz' > baseline-running.config
```

If this gate fails, restore stock boot and stop. Do not add DroidSpaces changes.

## Gate 5 — DroidSpaces config compile

Apply only the reviewed DroidSpaces fragment/required non-GKI changes.

Pass when final `.config` includes at least:

```text
CONFIG_NAMESPACES=y
CONFIG_PID_NS=y
CONFIG_IPC_NS=y
CONFIG_UTS_NS=y
CONFIG_NET_NS=y
```

and the project decision for these is explicit:

```text
CONFIG_USER_NS=y
CONFIG_VETH=y
```

Review the entire stock-vs-DroidSpaces config diff before compiling.

## Gate 6 — Modified-kernel device smoke test

After manual flash, repeat all Gate 4 Android checks before opening DroidSpaces.

## Gate 7 — DroidSpaces requirements

Run:

```sh
adb shell su -c '/data/local/Droidspaces/bin/droidspaces check'
```

Mandatory pass criteria include PID and IPC namespaces. Record the complete check output, not only the previously failing lines.

## Gate 8 — Minimal container

Start with a minimal ARM64 container and conservative networking.

Validate:

```sh
uname -a
cat /etc/os-release
ps
mount
ip addr
```

Do not install Docker yet.

## Gate 9 — Full service container

Only after the minimal container is stable:

- Debian/Ubuntu ARM64;
- init/systemd behavior;
- package manager;
- sshd;
- tailscaled;
- tmux/Codex workload.

## Gate 10 — Nested containers

Docker/Podman is last. Verify kernel/cgroup/network prerequisites first and record any DroidSpaces-specific legacy-kernel requirements.

## Failure discipline

At every failure:

1. stop at the failing gate;
2. record evidence;
3. revert to the last known-good artifact if the phone is affected;
4. change one variable only;
5. rerun the same gate.
