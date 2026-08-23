#!/usr/bin/env python3
"""Compare two tar archives without extracting platform-sensitive paths."""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from pathlib import Path


def normalized_name(name: str) -> str:
    while name.startswith("./"):
        name = name[2:]
    return name.rstrip("/")


def archive_manifest(path: Path) -> dict[str, tuple[str, int, str]]:
    manifest: dict[str, tuple[str, int, str]] = {}
    with tarfile.open(path, mode="r:*") as archive:
        for member in archive:
            name = normalized_name(member.name)
            if not name or member.isdir():
                continue
            if member.isfile():
                source = archive.extractfile(member)
                if source is None:
                    raise RuntimeError(f"cannot read regular file: {member.name}")
                digest = hashlib.sha256()
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    digest.update(chunk)
                value = ("file", member.size, digest.hexdigest())
            elif member.issym():
                value = ("symlink", 0, member.linkname)
            elif member.islnk():
                value = ("hardlink", 0, normalized_name(member.linkname))
            else:
                value = (f"type-{member.type!r}", member.size, member.linkname)
            if name in manifest and manifest[name] != value:
                raise RuntimeError(f"conflicting duplicate archive entry: {name}")
            manifest[name] = value
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--third", type=Path)
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    left = archive_manifest(args.left)
    right = archive_manifest(args.right)
    left_names = set(left)
    right_names = set(right)
    common = left_names & right_names
    changed = sorted(name for name in common if left[name] != right[name])
    only_left = sorted(left_names - right_names)
    only_right = sorted(right_names - left_names)

    result = {
        "left": str(args.left),
        "right": str(args.right),
        "left_entries": len(left),
        "right_entries": len(right),
        "common_entries": len(common),
        "identical_common_entries": len(common) - len(changed),
        "changed_common_entries": len(changed),
        "only_left_entries": len(only_left),
        "only_right_entries": len(only_right),
        "changed": [
            {"path": name, "left": left[name], "right": right[name]}
            for name in changed[: args.limit]
        ],
        "only_left": only_left[: args.limit],
        "only_right": only_right[: args.limit],
        "output_truncated": any(
            len(items) > args.limit for items in (changed, only_left, only_right)
        ),
    }

    if args.third:
        third = archive_manifest(args.third)
        classifications: dict[str, list[str]] = {}
        all_names = left_names | right_names | set(third)
        for name in sorted(all_names):
            values = (left.get(name), right.get(name), third.get(name))
            if values[0] == values[1] == values[2]:
                label = "all_same"
            elif values[0] == values[1] != values[2]:
                label = "left_right_same"
            elif values[0] == values[2] != values[1]:
                label = "left_third_same"
            elif values[1] == values[2] != values[0]:
                label = "right_third_same"
            elif len({value for value in values if value is not None}) == 3:
                label = "all_different"
            else:
                presence = "".join(
                    marker for marker, value in zip("LRT", values) if value is not None
                )
                label = f"presence_{presence}"
            classifications.setdefault(label, []).append(name)
        result["third"] = str(args.third)
        result["three_way"] = {
            label: {
                "count": len(names),
                "paths": names[: args.limit] if label != "all_same" else [],
                "truncated": label != "all_same" and len(names) > args.limit,
            }
            for label, names in sorted(classifications.items())
        }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if changed or only_left or only_right else 0


if __name__ == "__main__":
    raise SystemExit(main())
