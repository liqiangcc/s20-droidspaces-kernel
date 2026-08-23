# Codex Work Handoff

## Current state

- Gate 0: complete from the real SM-G9810/x1q device.
- Gate 1: formally `BLOCKED`; no exact SM-G9810 `G9810ZCSBHXJ2` Samsung OSRC
  package has been identified.
- Experimental Gate 2: owner-authorized reconstructed-source stock build
  succeeded twice with identical same-output-tree hashes. Formal Gate 2 is not
  passed because clean-tree signing-key reproducibility and Gate 1 remain
  unresolved. See `evidence/gate2-stock-baseline.md`.
- Gate 3 and all packaging/flashing work: not started and not authorized.

The current reconstructed source archive is:

```text
SM-G9810_X1Q_CHN_HXJ2_RECONSTRUCTED_v3_Kernel.tar.gz
SHA256=b8f997f84ef48d38b3d4ca1e848eb099be261ffd084c459f188ed482d8bf4dc7
```

The authoritative build tree must be on a case-sensitive Linux filesystem.
NTFS/DrvFS collapsed required pairs such as `xt_DSCP.c` and `xt_dscp.c`.

## Stop point

Stop after documenting, committing, and pushing the experimental Gate 2
result. Do not create or unpack `boot.img`, repack any partition image, run
Odin/Heimdall, or write to a block device.

Formal progression to Gate 3 requires a separate owner decision after review
of these risks:

- exact firmware/source mapping remains unresolved;
- the available Clang is 10.0.9 while stock reports 10.0.6;
- x1q China DTS provenance is from the older official HK package;
- Samsung internal `secgetspf` metadata and the Android-tree `perflog.h` input
  are unavailable;
- a verified stock boot backup and recovery path is mandatory before any
  future flash candidate can be considered.
