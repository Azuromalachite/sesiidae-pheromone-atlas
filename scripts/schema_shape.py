"""The record shape of the schemas, and the v0.1 freeze check.

The shape of a schema is, at every JSON path, its `required` list, its
`enum` values and its `properties` names. The v0.1 shape is recorded in
schemas/frozen-v0.1.json. A later schema passes the freeze when it is
additive only:

* every frozen path still exists;
* `required` is unchanged (a new required field breaks old records);
* `enum` is a superset (a removed value breaks old records);
* `properties` is a superset (a removed field breaks readers).

New paths, new optional properties and new enum values are allowed. A
breaking change needs a new frozen file, a schema_version bump in
scripts/build_release.py and a CHANGELOG entry, all in one commit.

    python scripts/schema_shape.py --write   # record the current shape (only when deliberately re-freezing)
    python scripts/schema_shape.py           # check against the frozen shape
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
FROZEN = SCHEMAS / "frozen-v0.1.json"


def shape(node, path="", out=None):
    out = {} if out is None else out
    if isinstance(node, dict):
        entry = {}
        if isinstance(node.get("required"), list):
            entry["required"] = sorted(node["required"])
        if isinstance(node.get("enum"), list):
            entry["enum"] = sorted(json.dumps(v) for v in node["enum"])
        if isinstance(node.get("properties"), dict):
            entry["properties"] = sorted(node["properties"])
        if entry:
            out[path or "/"] = entry
        for k, v in node.items():
            shape(v, f"{path}/{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            shape(v, f"{path}/{i}", out)
    return out


def current():
    return {p.name: shape(json.loads(p.read_text(encoding="utf-8")))
            for p in sorted(SCHEMAS.glob("*.schema.json"))}


def breaks(frozen, now):
    out = []
    for name, paths in frozen.items():
        if name not in now:
            out.append(f"{name}: schema removed")
            continue
        for path, want in paths.items():
            have = now[name].get(path)
            if have is None:
                out.append(f"{name} {path}: removed")
                continue
            if "required" in want and have.get("required") != want["required"]:
                out.append(f"{name} {path}: required changed {want['required']} -> {have.get('required')}")
            for key in ("enum", "properties"):
                lost = set(want.get(key, [])) - set(have.get(key, []))
                if lost:
                    out.append(f"{name} {path}: {key} lost {sorted(lost)}")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="record the current shape as frozen")
    args = ap.parse_args(argv)
    if args.write:
        FROZEN.write_text(json.dumps(current(), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {FROZEN.relative_to(ROOT)}")
        return 0
    problems = breaks(json.loads(FROZEN.read_text(encoding="utf-8")), current())
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        return 1
    print("schemas are additive over the v0.1 shape")
    return 0


if __name__ == "__main__":
    sys.exit(main())
