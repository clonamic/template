#!/usr/bin/env python3
"""Copy the spec and report templates into the clonamic-harness plugin.

Usage: sync_to_plugin.py [--check] [--plugin PATH]

The plugin repository defaults to the sibling ../plugin. When it does not exist the script
does nothing and exits 0. --check writes nothing and exits 1 when any copy differs.
"""

import argparse
import sys
from pathlib import Path

if sys.version_info < (3, 12):
    sys.exit("Python 3.12 or newer is required (for example: uv python install 3.12).")

ROOT = Path(__file__).resolve().parents[1]
COPIES = {
    "작업명세서.md": "clonamic-harness/skills/clonamic-spec/references/work-spec.md",
    "개발명세서.md": "clonamic-harness/skills/clonamic-spec/references/dev-spec.md",
    "보고서.md": "clonamic-harness/skills/clonamic-finish/references/report.md",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report differences without writing")
    parser.add_argument("--plugin", type=Path, default=ROOT.parent / "plugin", help="plugin repository root")
    args = parser.parse_args()

    plugin = args.plugin.resolve()
    if not plugin.is_dir():
        print(f"skip: plugin repository not found at {plugin}")
        return 0

    stale = []
    for source, target in COPIES.items():
        data = (ROOT / source).read_bytes()
        dest = plugin / target
        if dest.is_file() and dest.read_bytes() == data:
            continue
        stale.append(target)
        if not args.check:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)

    verb = "differs" if args.check else "updated"
    for target in stale:
        print(f"{verb}: {target}")
    if not stale:
        print("in sync")
    return 1 if args.check and stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
