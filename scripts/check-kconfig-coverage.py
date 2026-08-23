#!/usr/bin/env python3
"""Statically check whether a tarred source tree defines config symbols."""

from __future__ import annotations

import argparse
import json
import re
import tarfile
from pathlib import Path, PurePosixPath


DEFINITION = re.compile(
    r"^\s*(?:config|menuconfig)\s+([A-Za-z0-9_]+)\s*$", re.MULTILINE
)
ENABLED = re.compile(r"^(CONFIG_[A-Za-z0-9_]+)=(.*)$")
DISABLED = re.compile(r"^# (CONFIG_[A-Za-z0-9_]+) is not set$")


def source_definitions(path: Path) -> set[str]:
    definitions: set[str] = set()
    with tarfile.open(path, "r:*") as archive:
        for member in archive:
            if not member.isfile() or not PurePosixPath(member.name).name.startswith(
                "Kconfig"
            ):
                continue
            stream = archive.extractfile(member)
            if stream is None:
                raise RuntimeError(f"cannot read {member.name}")
            text = stream.read().decode("utf-8", errors="replace")
            definitions.update("CONFIG_" + name for name in DEFINITION.findall(text))
    return definitions


def observed_config(path: Path) -> dict[str, str]:
    symbols: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="strict").splitlines():
        match = ENABLED.match(line)
        if match:
            symbols[match.group(1)] = match.group(2)
            continue
        match = DISABLED.match(line)
        if match:
            symbols[match.group(1)] = "<not set>"
    return symbols


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_archive", type=Path)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()

    definitions = source_definitions(args.source_archive)
    config = observed_config(args.config)
    missing = sorted(set(config) - definitions)
    active_missing = [name for name in missing if config[name] != "<not set>"]
    result = {
        "source_archive": str(args.source_archive),
        "config": str(args.config),
        "defined_symbols": len(definitions),
        "config_symbols": len(config),
        "missing_symbols": len(missing),
        "active_missing_symbols": len(active_missing),
        "active_missing": active_missing,
        "disabled_missing": [name for name in missing if name not in active_missing],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if active_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
