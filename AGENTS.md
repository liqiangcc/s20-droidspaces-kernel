# AGENTS.md

## Mission

Adapt the stock Samsung Galaxy S20 5G SM-G9810 (`x1q`) kernel for DroidSpaces with the smallest possible, reviewable change set.

## Non-negotiable workflow

1. **Source first.** Do not compile until the exact device firmware/build and matching Samsung Open Source kernel package are recorded in `docs/source-mapping.md`.
2. **Stock baseline first.** The first kernel build must use the stock defconfig with no DroidSpaces changes. Do not proceed to a modified kernel until the stock-baseline build artifacts are reproducible.
3. **One variable at a time.** Do not mix namespace changes with KernelSU/SUSFS/security-feature removals, performance tweaks, DTB changes, ramdisk changes, or unrelated patches.
4. **No automatic flashing.** Agents may prepare artifacts and commands, but must stop before any command that writes boot/recovery/vendor/system/userdata partitions.
5. **Always preserve rollback.** `boot-stock.img`, its SHA256, exact firmware identifiers, and recovery instructions are mandatory before a flash candidate can be called ready for manual testing.
6. **No unverified third-party kernel binaries.** Third-party S20 kernels may be studied for build techniques only unless their exact model/firmware compatibility and changes are independently reviewed.

## Required gates

- Gate 0: device/firmware baseline captured.
- Gate 1: matching Samsung source and defconfig identified.
- Gate 2: stock-baseline kernel compiles reproducibly.
- Gate 3: stock-baseline boot image is statically verified.
- Gate 4: DroidSpaces config fragment applies cleanly and final `.config` is verified.
- Gate 5: modified kernel compiles reproducibly.
- Gate 6: candidate boot image and rollback package are prepared.
- Gate 7: **manual owner approval before flash**.
- Gate 8: post-boot Android smoke tests.
- Gate 9: DroidSpaces requirement check.
- Gate 10: minimal container test; Docker is last.

## Evidence discipline

For every important decision, record:

- source URL / source package name;
- exact commit or package version where applicable;
- command executed;
- output or checksum;
- whether the result is observed, inferred, or still unverified.

Do not silently fill missing device facts from another `x1q` variant.
