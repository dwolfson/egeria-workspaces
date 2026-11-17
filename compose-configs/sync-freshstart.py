#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
"""Keep freshstart's Portal (PyegeriaWebHandler) in step with quickstart's (SHARE-3, option a).

Quickstart is always the source. Edit a shared file in
compose-configs/egeria-quickstart/PyegeriaWebHandler/, then run

    python3 compose-configs/sync-freshstart.py --write

to bring freshstart's copy up to date, and commit both. CI runs --check.

    --check            exit 1 and list what is wrong: drifted files (with the command that fixes them),
                       files the manifest does not classify, and manifest entries that are stale
    --write [PATH ...] copy quickstart -> freshstart for the `identical` and `transformed` entries
                       (all of them, or just the PATHs given), applying each entry's transforms
    --summary          print the count in each manifest category
    --strict           with --check, also fail on pending entries that are now in sync

The manifest, compose-configs/freshstart-sync-manifest.json, puts every file of either tree in exactly
one category (an explicit path beats a glob):

    identical    byte-identical in both trees
    transformed  identical after the entry's named transforms (see "transforms" in the manifest)
    pending      becomes identical/transformed when the named PR merges; reported, never fails. Once it is
                 in sync, --check notes that the entry should move to identical/transformed (a failure only
                 with --strict, so the named PR landing does not turn unrelated PRs red; CI does not pass it).
    by_design    differs on purpose, or exists in one tree only on purpose (reason given)
    not_yet      should be synced but is not yet (parity row given). Once a file listed by name is in
                 sync, --check fails until it is moved to identical, so the list only shrinks.

Transforms are plain byte substitutions over the whole file. In particular env-path replaces EVERY
"egeria-quickstart" in it, comments, docs and URLs included, so when an entry first uses env-path, read
the resulting freshstart file by eye.

Transform "fences" keeps freshstart-only blocks: lines from one containing FRESHSTART-ONLY BEGIN to one
containing FRESHSTART-ONLY END stay as they are, re-inserted after the line that precedes them (which
must occur exactly once in quickstart's text).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "compose-configs" / "freshstart-sync-manifest.json"
SOURCE = "compose-configs/egeria-quickstart/PyegeriaWebHandler"
TARGET = "compose-configs/egeria-freshstart/PyegeriaWebHandler"
CATEGORIES = ("identical", "transformed", "pending", "by_design", "not_yet")
SYNCED = ("identical", "transformed")
FENCE_BEGIN, FENCE_END = b"FRESHSTART-ONLY BEGIN", b"FRESHSTART-ONLY END"
FIX = "python3 compose-configs/sync-freshstart.py --write"
WALK_IGNORE = ("*__pycache__/*", "*.pyc", ".pytest_cache/*", "*/.pytest_cache/*", "logs/*", "*.log", "*.DS_Store",
               "._*", "*/._*")


class SyncError(Exception):
    pass


def _is_glob(p: str) -> bool:
    return any(c in p for c in "*?[")


def _files(repo: Path, sub: str) -> set[str]:
    """Tracked files under sub (relative to it); a plain walk when this is not a git checkout."""
    root = repo / sub
    try:
        out = subprocess.run(["git", "-C", str(repo), "ls-files", "-z", "--", sub],
                             capture_output=True, check=True).stdout.decode()
        rels = [p[len(sub) + 1:] for p in out.split("\0") if p]
        return {r for r in rels if (root / r).is_file()}
    except (OSError, subprocess.CalledProcessError):
        # not a checkout (e.g. a copied tree): skip what git would not track
        rels = (str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
        return {r for r in rels if not any(fnmatch.fnmatchcase(r, pat) for pat in WALK_IGNORE)}


def _entries(manifest: dict, cat: str) -> dict:
    v = manifest.get(cat, {})
    return {p: {} for p in v} if isinstance(v, list) else dict(v)


def classify(manifest: dict, path: str) -> list[str]:
    hits = [c for c in CATEGORIES if path in _entries(manifest, c)]
    if hits:
        return hits
    for c in CATEGORIES:
        for pat in _entries(manifest, c):
            if _is_glob(pat) and fnmatch.fnmatchcase(path, pat):
                return [c]
    return []


def _split_fences(data: bytes) -> tuple[list[bytes], list[tuple[bytes | None, list[bytes]]]]:
    """(lines outside fences, [(anchor line or None, block lines)])."""
    core, blocks, block = [], [], None
    for line in data.splitlines(keepends=True):
        if block is None and FENCE_BEGIN in line:
            block = [line]
            continue
        if block is not None:
            block.append(line)
            if FENCE_END in line:
                blocks.append((core[-1] if core else None, block))
                block = None
            continue
        core.append(line)
    if block is not None:
        raise SyncError("a FRESHSTART-ONLY BEGIN has no matching END")
    return core, blocks


def render(manifest: dict, entry: dict, src: bytes, dst: bytes | None) -> bytes:
    """Freshstart's expected content: quickstart's, transformed, with dst's fenced blocks put back."""
    names = entry.get("transforms", [])
    out = src
    for name in names:
        if name == "fences":
            continue
        if name not in manifest.get("transforms", {}):
            raise SyncError(f"unknown transform {name!r}")
        for old, new in manifest["transforms"][name]:
            out = out.replace(old.encode(), new.encode())
    if "fences" not in names:
        if dst is not None and FENCE_BEGIN in dst:
            # without the fences transform the block would be silently dropped on --write
            raise SyncError("freshstart's copy has a FRESHSTART-ONLY block but the entry has no 'fences' "
                            "transform; add 'fences' to its transforms (or remove the block) first")
        return out
    if dst is None:
        return out
    lines = out.splitlines(keepends=True)
    _, blocks = _split_fences(dst)
    for anchor, block in reversed(blocks):
        if anchor is None:
            at = 0
        else:
            idx = [i for i, l in enumerate(lines) if l == anchor]
            if len(idx) != 1:
                raise SyncError(f"the line before a FRESHSTART-ONLY block occurs {len(idx)} times in quickstart's "
                                f"text, so the block has no unique place: {anchor.decode(errors='replace').strip()!r}")
            at = idx[0] + 1
        lines[at:at] = block
    return b"".join(lines)


def check(repo: Path = REPO, manifest_path: Path = MANIFEST, strict: bool = False) -> tuple[list[str], list[str]]:
    """(failures, notes). No failures means freshstart is in sync with what the manifest says."""
    manifest = json.loads(manifest_path.read_text())
    src_files, dst_files = _files(repo, SOURCE), _files(repo, TARGET)
    fail, note, drifted = [], [], []

    for path in sorted(src_files | dst_files):
        cats = classify(manifest, path)
        where = "both" if path in src_files and path in dst_files else ("quickstart" if path in src_files else "freshstart")
        if not cats:
            fail.append(f"unclassified ({where}): {path} — add it to {manifest_path.name}")
        elif len(cats) > 1:
            fail.append(f"in more than one category ({', '.join(cats)}): {path}")

    for cat in CATEGORIES:
        if cat == "pending":
            continue  # a pending file may arrive with its PR
        for pat in _entries(manifest, cat):
            hit = ([p for p in src_files | dst_files if fnmatch.fnmatchcase(p, pat)] if _is_glob(pat)
                   else ([pat] if pat in src_files | dst_files else []))
            if not hit:
                fail.append(f"stale {cat} entry, matches no file in either tree: {pat}")

    def in_sync(path: str, entry: dict) -> bool:
        if path not in src_files or path not in dst_files:
            return False
        dst = (repo / TARGET / path).read_bytes()
        expected = render(manifest, entry, (repo / SOURCE / path).read_bytes(), dst)
        return expected == dst

    for cat in SYNCED:
        for path, entry in _entries(manifest, cat).items():
            if path not in src_files:
                if path in dst_files:
                    fail.append(f"{cat}: {path} is gone from quickstart; delete freshstart's copy or reclassify it")
                continue
            try:
                ok = in_sync(path, entry)
            except SyncError as exc:
                fail.append(f"{cat}: {path}: {exc}")
                continue
            if not ok:
                drifted.append(path)
    if drifted:
        fail.append("drifted from quickstart (quickstart is the source):\n" +
                    "\n".join(f"    {p}" for p in drifted) +
                    f"\n  fix: {FIX}   (or: {FIX} " + " ".join(f"'{p}'" for p in drifted) + ")")

    for path, entry in _entries(manifest, "pending").items():
        try:
            ok = in_sync(path, entry)
        except SyncError:
            ok = False
        if ok:
            (fail if strict else note).append(f"pending ({entry.get('after', '?')}) is now in sync: move {path} to "
                        f"{'transformed' if entry.get('transforms') else 'identical'}")
        else:
            note.append(f"pending until {entry.get('after', '?')}: {path}")

    for path in _entries(manifest, "not_yet"):
        if not _is_glob(path) and path in src_files and path in dst_files and \
                (repo / SOURCE / path).read_bytes() == (repo / TARGET / path).read_bytes():
            fail.append(f"not_yet entry is now identical: move {path} to identical")
    for path in sorted(src_files & dst_files):
        if classify(manifest, path) == ["not_yet"] and path not in _entries(manifest, "not_yet") and \
                (repo / SOURCE / path).read_bytes() == (repo / TARGET / path).read_bytes():
            fail.append(f"identical but only covered by a not_yet glob: add {path} to identical")
        if classify(manifest, path) == ["by_design"] and \
                (repo / SOURCE / path).read_bytes() == (repo / TARGET / path).read_bytes():
            note.append(f"by_design file is identical (consider moving it to identical): {path}")
    return fail, note


def write(paths: list[str], repo: Path = REPO, manifest_path: Path = MANIFEST) -> list[str]:
    """Copy quickstart -> freshstart for synced entries (all, or the given paths). Returns the paths changed."""
    manifest = json.loads(manifest_path.read_text())
    synced = {p: e for cat in SYNCED for p, e in _entries(manifest, cat).items()}
    unknown = [p for p in paths if p not in synced]
    if unknown:
        raise SyncError("not an identical/transformed entry (classify it in the manifest first): " + ", ".join(unknown))
    changed = []
    for path in paths or sorted(synced):
        src_p, dst_p = repo / SOURCE / path, repo / TARGET / path
        if not src_p.is_file():
            raise SyncError(f"{path}: not in quickstart")
        dst = dst_p.read_bytes() if dst_p.is_file() else None
        new = render(manifest, synced[path], src_p.read_bytes(), dst)
        if new != dst:
            dst_p.parent.mkdir(parents=True, exist_ok=True)
            dst_p.write_bytes(new)
            if dst is None:
                dst_p.chmod(src_p.stat().st_mode & 0o777)
            changed.append(path)
    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", nargs="*", metavar="PATH")
    g.add_argument("--summary", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="with --check, also fail on pending entries that are now in sync")
    ap.add_argument("-v", "--verbose", action="store_true", help="with --check, also list pending/notes")
    args = ap.parse_args(argv)
    try:
        if args.summary:
            manifest = json.loads(MANIFEST.read_text())
            for c in CATEGORIES:
                print(f"{c:12} {len(_entries(manifest, c))}")
            return 0
        if args.write is not None:
            changed = write(args.write)
            print("\n".join(f"wrote {TARGET}/{p}" for p in changed) or "freshstart already in sync")
            return 0
        fail, note = check(strict=args.strict)
    except SyncError as exc:
        print(f"sync-freshstart: {exc}", file=sys.stderr)
        return 2
    if args.verbose or not fail:
        for n in note:
            print(f"note: {n}")
    for f in fail:
        print(f"FAIL: {f}")
    print("freshstart Portal is in sync with quickstart" if not fail else
          f"\n{len(fail)} problem(s). Quickstart is the source: edit it, then run {FIX}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
