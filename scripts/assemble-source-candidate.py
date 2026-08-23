#!/usr/bin/env python3
"""Assemble the documented experimental x1q China source candidate."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import tarfile
from pathlib import Path


HK_PATHS = (
    "arch/arm64/Kconfig.projects",
    "arch/arm64/configs/vendor/x1q_chn_hkx_defconfig",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r07.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r08.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r09.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r12.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r13.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-chn-overlay-r14.dts",
)

CHN_COMMON_PATHS = (
    "drivers/gpu/drm/drm_edid.c",
    "drivers/usb/gadget/function/f_ss_mon_gadget.c",
    "include/linux/ologk.h",
    "techpack/display/msm/dp/dp_display.c",
    "techpack/display/msm/dp/secdp.h",
)

REMOVE_KOR_PATHS = {
    "arch/arm64/configs/vendor/x1q_kor_singlex_defconfig",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-kor-overlay-r13.dts",
    "arch/arm64/boot/dts/samsung/x1q/kona-sec-x1q-kor-overlay-r14.dts",
}


def normalized_name(name: str) -> str:
    while name.startswith("./"):
        name = name[2:]
    return name.rstrip("/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def member_index(archive: tarfile.TarFile) -> dict[str, tarfile.TarInfo]:
    return {normalized_name(member.name): member for member in archive.getmembers()}


def add_member(
    output: tarfile.TarFile,
    source: tarfile.TarFile,
    member: tarfile.TarInfo,
    target_name: str | None = None,
) -> None:
    copied = copy.copy(member)
    if target_name is not None:
        copied.name = "./" + target_name
    stream = source.extractfile(member) if member.isfile() else None
    output.addfile(copied, stream)


def provenance_text(args: argparse.Namespace) -> str:
    hk_lines = "\n".join(f"- {path}" for path in HK_PATHS)
    chn_lines = "\n".join(f"- {path}" for path in CHN_COMMON_PATHS)
    removed_lines = "\n".join(f"- {path}" for path in sorted(REMOVE_KOR_PATHS))
    return f"""# Experimental Candidate Provenance

This is not an exact Samsung release and must not be represented as one.
It was assembled for static analysis only; assembly did not compile a kernel.

Base archive:
- {args.kor}
- SHA256: {sha256(args.kor)}

SM-G9810 HK x1q China project overlays:
{hk_lines}

Source archive:
- {args.hk}
- SHA256: {sha256(args.hk)}

China-common files corroborated by both HK x1q and CHN HXJ2 y2q:
{chn_lines}

Source archive:
- {args.chn}
- SHA256: {sha256(args.chn)}

Removed KOR-only target files:
{removed_lines}

Known unresolved issue:
- The x1q China DTS and project defconfig originate from the older HK HWH9
  package because Samsung did not publish the exact SM-G9810 HXJ2 archive.
- The inherited build_kernel.sh still identifies the KOR defconfig and must
  not be executed for this candidate.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kor", required=True, type=Path)
    parser.add_argument("--hk", required=True, type=Path)
    parser.add_argument("--chn", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    overlay_paths = set(HK_PATHS) | set(CHN_COMMON_PATHS)
    with (
        tarfile.open(args.kor, "r:*") as kor,
        tarfile.open(args.hk, "r:*") as hk,
        tarfile.open(args.chn, "r:*") as chn,
        args.output.open("wb") as raw_output,
        gzip.GzipFile(filename="", mode="wb", fileobj=raw_output, mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w|", format=tarfile.GNU_FORMAT) as output,
    ):
        hk_members = member_index(hk)
        chn_members = member_index(chn)

        for member in kor:
            name = normalized_name(member.name)
            if name in REMOVE_KOR_PATHS or name in overlay_paths:
                continue
            add_member(output, kor, member)

        for path in HK_PATHS:
            if path not in hk_members:
                raise RuntimeError(f"missing HK overlay path: {path}")
            add_member(output, hk, hk_members[path], path)

        for path in CHN_COMMON_PATHS:
            if path not in chn_members:
                raise RuntimeError(f"missing CHN common path: {path}")
            add_member(output, chn, chn_members[path], path)

        provenance = provenance_text(args).encode("utf-8")
        info = tarfile.TarInfo("CANDIDATE_PROVENANCE.md")
        info.size = len(provenance)
        info.mode = 0o644
        info.mtime = 0
        output.addfile(info, io.BytesIO(provenance))

    print(f"output={args.output}")
    print(f"size={args.output.stat().st_size}")
    print(f"sha256={sha256(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
