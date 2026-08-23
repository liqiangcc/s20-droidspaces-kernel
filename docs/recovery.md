# Recovery Plan

## Principle

No experimental kernel is flash-ready until rollback has been prepared first.

## Required backup set

Keep copies outside the phone of:

- current known-good `boot.img`;
- SHA256 of the boot image;
- exact firmware identifiers from `docs/device-baseline.md`;
- stock kernel config from `/proc/config.gz`;
- original Samsung firmware package/source references needed to recover;
- the exact command/tool sequence used to restore boot.

Suggested local naming:

```text
recovery/
├── boot-stock.img
├── boot-stock.img.sha256
├── stock.config
├── device-properties.txt
└── restore-notes.md
```

Do not commit private/personal recovery artifacts or firmware binaries to this public repository unless their redistribution is explicitly allowed.

## Flash scope

The intended experiment changes only the boot/kernel path. Do not intentionally modify:

- `userdata`;
- `system`;
- `vendor`;
- `product`;
- modem/baseband;
- CSC;
- partition table.

Do not use NAND erase or repartition options.

## Bootloop response

If an experimental kernel fails to boot:

1. stop repeated boot attempts if possible;
2. enter the previously verified Samsung recovery/download path;
3. restore the exact known-good boot image/package;
4. boot Android and verify data/root/network/ADB state;
5. record the failed candidate SHA256 and failure symptoms;
6. do not retry with additional changes bundled together.

## Data safety

Replacing a boot image normally does not erase `userdata`, but a kernel failure can make encrypted data temporarily inaccessible. Important data should therefore be backed up independently before the first flash.

Bootloader unlock/relock and full-firmware/CSC operations have different data-loss semantics and are outside this project's normal test loop.
