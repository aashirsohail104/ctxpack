"""CLI entry point and orchestrator.

Wires the scanner, ranker, packer, manifest, and report together.
Exit codes follow SPEC.md:

* 0 — success
* 1 — invalid arguments / write error
* 2 — path not found or unreadable
"""

import argparse
import json
import os
import sys
import time
from typing import List, Optional, Sequence

from .manifest import build_manifest, one_line_summary
from .packer import bundle_files
from .ranker import rank_files
from .report import generate_report
from .scanner import scan_files
from .tokenize import parse_task
from .tree import build_tree
from .utils import count_tokens


class CtxArgumentParser(argparse.ArgumentParser):
    """argparse that emits one-line ctxpack errors instead of tracebacks."""

    def error(self, message: str) -> None:  # pragma: no cover - argparse path
        sys.stderr.write(f"ctxpack: error: {message}\n")
        sys.exit(1)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse and validate CLI args. Exits with code 1 or 2 on bad input."""
    parser = CtxArgumentParser(prog="ctxpack", add_help=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--budget", required=True)
    parser.add_argument("--out", default=None)
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--report", default=None)

    args = parser.parse_args(argv)

    try:
        budget = int(args.budget)
    except ValueError:
        sys.stderr.write("ctxpack: error: --budget must be an integer\n")
        sys.exit(1)

    if budget <= 0:
        sys.stderr.write("ctxpack: error: --budget must be a positive integer\n")
        sys.exit(1)

    if not os.path.exists(args.path):
        sys.stderr.write(f"ctxpack: error: Path not found: {args.path}\n")
        sys.exit(2)

    if not os.path.isdir(args.path):
        sys.stderr.write(f"ctxpack: error: Path is not a directory: {args.path}\n")
        sys.exit(2)

    args.budget = budget
    return args


def _write_bytes(path: str, data: bytes, label: str) -> None:
    try:
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        sys.stderr.write(f"ctxpack: error: cannot write --{label}: {path} -- {e}\n")
        sys.exit(1)


def _write_stdout(bundle: str) -> None:
    try:
        sys.stdout.write(bundle)
    except UnicodeEncodeError:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(bundle)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    t0 = time.time()
    try:
        included_files, excluded_from_scan = scan_files(args.path)
    except OSError as e:
        sys.stderr.write(f"ctxpack: error: cannot read path: {args.path} -- {e}\n")
        return 2
    t1 = time.time()

    task_keywords = parse_task(args.task)
    ranked, excluded_from_rank = rank_files(included_files, task_keywords)
    t2 = time.time()

    tree_str = build_tree(args.path)
    bundle, used, included_in_bundle, excluded_from_bundle, tree_included = bundle_files(
        ranked, args.budget, tree_str, args.task, args.path
    )
    t3 = time.time()

    all_excluded: List[dict] = excluded_from_scan + excluded_from_rank + excluded_from_bundle

    manifest_included = []
    for entry in included_in_bundle:
        me = {
            "path": entry["path"],
            "tokens": entry["tokens"],
            "reason": entry["reason"],
        }
        if entry.get("truncated"):
            me["truncated"] = True
        manifest_included.append(me)

    if not tree_included:
        tree_full = f"## Project Structure\n\n```\n{tree_str}\n```\n\n"
        tree_cost = count_tokens(tree_full)
        if tree_cost > args.budget:
            reason = f"Tree too large ({tree_cost} tokens) for remaining budget"
        else:
            reason = "Tree excluded to stay within budget"
        all_excluded.append({"path": "<directory tree>", "reason": reason})

    if args.out:
        _write_bytes(args.out, bundle.encode("utf-8"), "out")
    else:
        _write_stdout(bundle)

    if args.manifest:
        manifest = build_manifest(args.budget, used, manifest_included, all_excluded)
        payload = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        _write_bytes(args.manifest, payload, "manifest")
    else:
        sys.stderr.write(one_line_summary(
            len(manifest_included), used, args.budget, len(all_excluded)
        ))

    if args.report:
        timing = {
            "scan": round(t1 - t0, 3),
            "rank": round(t2 - t1, 3),
            "bundle": round(t3 - t2, 3),
            "total": round(t3 - t0, 3),
        }
        ranked_preview = [(p, s, t) for p, _, s, t in ranked[:100]]
        report_html = generate_report(
            bundle, used, args.budget, manifest_included, all_excluded,
            ranked_preview, tree_str, args.task, args.path, timing,
        )
        _write_bytes(args.report, report_html.encode("utf-8"), "report")

    return 0


if __name__ == "__main__":
    sys.exit(main())
