# Adaptation Architecture

```text
SM-G9810 stock firmware
        ↓
matching Samsung Open Source kernel
        ↓
stock device defconfig
        ↓
Stock Baseline Build
        ↓
prove reproducible build + packaging
        ↓
minimal DroidSpaces config delta
        ↓
Modified Kernel Build
        ↓
static boot artifact verification
        ↓
MANUAL flash gate
        ↓
Android smoke test
        ↓
DroidSpaces requirements check
        ↓
minimal container
        ↓
services
        ↓
Docker/Podman last
```

The architecture deliberately keeps Android/vendor integration stock and treats DroidSpaces support as a kernel-capability adaptation rather than a ROM replacement project.
