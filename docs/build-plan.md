# Build Plan

## Build philosophy

The goal is not to build a feature-rich custom kernel. The goal is to prove that the stock Samsung kernel can be rebuilt reproducibly, then introduce the smallest DroidSpaces-specific delta.

## Phase 0 — Host setup

Preferred build host:

- x86_64 Linux;
- Ubuntu 22.04 / Debian-family environment;
- 8 CPU cores recommended;
- 16 GB RAM recommended;
- 80 GB free disk recommended.

Install only the dependencies required by Samsung's source package README and the selected toolchain. Do not assume a toolchain from an unrelated `x1q` project.

## Phase 1 — Stock-baseline build

1. Download and checksum the Samsung source package selected in `docs/source-mapping.md`.
2. Read the Samsung build instructions before modifying anything.
3. Identify the device defconfig.
4. Build using the stock defconfig with **zero DroidSpaces changes**.
5. Save:
   - compiler/toolchain versions;
   - build command;
   - final `.config`;
   - `arch/arm64/boot/Image` (or source-defined equivalent);
   - build log;
   - SHA256 for every artifact.
6. Compare the generated config against the captured `stock.config` and explain every difference before continuing.

A successful compile alone does not pass this phase. The baseline must be understood well enough to distinguish expected generated-config differences from accidental configuration drift.

## Phase 2 — DroidSpaces config build

After the stock baseline is accepted:

1. apply `configs/droidspaces.fragment`;
2. run the source tree's normal config resolution (`olddefconfig` or source-specific equivalent);
3. verify the final `.config` with `scripts/verify-droidspaces-config.sh`;
4. review the complete config diff versus the accepted stock baseline;
5. compile using exactly the same source/toolchain/build procedure as Phase 1.

Do not change source revision, compiler, ramdisk, packaging method, and kernel configuration in the same experiment.

## Phase 3 — Boot image preparation

The intended packaging model is:

```text
current known-good boot image
├── original header/layout
├── original ramdisk
├── original cmdline
├── original vendor integration
└── newly compiled kernel payload only
```

The exact Samsung boot-image layout must be inspected before packaging. Do not assume a generic Pixel-style `boot.img` layout.

Before a candidate is called flash-ready, produce:

- original boot image SHA256;
- candidate boot image SHA256;
- unpacked metadata diff;
- kernel payload diff;
- proof that userdata/system/vendor partitions are not part of the flash plan;
- rollback command/package.

## Phase 4 — Stop for manual approval

Automated work ends here. No script in this repository should automatically write a phone partition.
