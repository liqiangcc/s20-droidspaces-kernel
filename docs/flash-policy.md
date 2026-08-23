# Flash Policy

This repository deliberately separates **artifact preparation** from **device flashing**.

## Agents may

- inspect device properties and captured config;
- fetch and review matching Samsung source;
- prepare build environments;
- compile stock and modified kernels;
- unpack/repack boot artifacts;
- compare metadata/configs;
- produce checksums and recovery instructions;
- prepare exact manual flash commands for review.

## Agents must not

- invoke Odin/Heimdall/fastboot or any write operation against a phone partition;
- overwrite `boot`, `recovery`, `vendor`, `system`, `product`, `userdata`, DTBO, modem, CSC, or partition tables;
- relock the bootloader;
- erase/repartition/NAND-erase;
- declare an artifact safe merely because compilation succeeded.

## Manual approval checkpoint

Before a flash, review all of the following together:

1. exact device/firmware match;
2. source package and defconfig;
3. stock-baseline proof;
4. complete config diff;
5. boot-image metadata diff;
6. candidate SHA256;
7. known-good stock boot SHA256;
8. tested recovery path.

Only then should the owner choose whether to perform the flash manually.
