"""Build the Atlas's machine-readable exports, and a release bundle on demand.

Two layers (docs/releases-and-occurrences.md):

* derived/ holds outputs that depend on the records only: one JSONL file per
  record kind, the taxon x layer matrix, summary.json and SHA256SUMS. They are
  committed, and CI runs --check. They carry no date, commit, tag or DOI, so
  the check is stable across commits.
* dist/sesiidae-atlas-v<version>/ is a release bundle: derived/ plus schemas,
  licences, CITATION.cff, CHANGELOG.md and manifest.json. Only the manifest
  holds release metadata (version, tag, commit, commit date). Bundles are not
  committed. No DOI is minted here.

    python scripts/build_release.py                    # refresh derived/
    python scripts/build_release.py --check            # exit 1 if derived/ is stale
    python scripts/build_release.py --bundle 0.1.0     # needs a clean tree at tag v0.1.0
    python scripts/build_release.py --bundle 0.1.0-rc1 --allow-untagged   # test the process

Every output is byte-deterministic: records sorted by ID, JSON with sorted
keys, LF line endings, UTF-8, no timestamps.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import atlas_validate as av  # noqa: E402
import build_taxon_layers as btl  # noqa: E402
import build_tables as bt  # noqa: E402

DERIVED = ROOT / "derived"
SCHEMA_VERSION = "0.1"   # the frozen record shape (schemas/frozen-v0.1.json); a breaking change bumps it
BUNDLE_EXTRA = ["CITATION.cff", "CHANGELOG.md", "LICENSE", "LICENSE-DATA.md", "README.md", "requirements.lock.txt"]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def jsonl(records):
    return "".join(json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n" for r in records)


def derived_files(data):
    """{relative path: bytes} for everything in derived/ except README.md."""
    records, findings = av.load_root(data)
    if findings:
        raise SystemExit("records do not load: " + "; ".join(f"{f.code} {f.path}" for f in findings))
    problems = av.validate(data)
    if problems:
        raise SystemExit(f"records do not validate ({len(problems)} findings); run atlas_validate.py first")
    out = {}
    counts = {}
    for kind in sorted(av.KINDS):
        recs = [rec for _, (_, rec) in sorted(records[kind].items())]
        counts[kind] = len(recs)
        out[f"{kind}.jsonl"] = jsonl(recs).encode("utf-8")
    out["taxon_layers.tsv"] = btl.build(data).encode("utf-8")
    for name, text in bt.build(data).items():
        out[name] = text.encode("utf-8")
    generators = sorted({json.dumps(c["generated"]["generator"], sort_keys=True)
                         for _, (_, c) in records["compounds"].items() if c.get("generated")})
    schemas = {p.name: sha256(p.read_bytes()) for p in sorted((ROOT / "schemas").glob("*.json"))}
    summary = {"schema_version": SCHEMA_VERSION, "record_counts": counts,
               "compound_generators": [json.loads(g) for g in generators], "schemas_sha256": schemas,
               "note": "Content-derived only: no date, commit, tag or DOI. Release metadata is in a bundle's manifest.json."}
    out["summary.json"] = (json.dumps(summary, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    out["SHA256SUMS"] = "".join(f"{sha256(out[n])}  {n}\n" for n in sorted(out)).encode("utf-8")
    return out


def write_derived(files):
    for name, data in files.items():
        (DERIVED / name).parent.mkdir(parents=True, exist_ok=True)
        (DERIVED / name).write_bytes(data)


def check_derived(files):
    stale = [n for n, data in files.items() if not (DERIVED / n).exists() or (DERIVED / n).read_bytes() != data]
    known = set(files) | {"README.md"}
    extra = sorted(p.relative_to(DERIVED).as_posix() for p in DERIVED.rglob("*")
                   if p.is_file() and p.relative_to(DERIVED).as_posix() not in known)
    return stale, extra


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def bundle(version, allow_untagged, out_root):
    if git("status", "--porcelain"):
        raise SystemExit("working tree is not clean: commit first, so the bundle matches a commit")
    commit = git("rev-parse", "HEAD")
    tags = git("tag", "--points-at", "HEAD").split()
    tag = f"v{version}"
    if tag not in tags and not allow_untagged:
        raise SystemExit(f"HEAD is not tagged {tag}; tag it, or pass --allow-untagged for a test bundle")
    files = derived_files(ROOT / "data")
    stale, extra = check_derived(files)
    if stale or extra:
        raise SystemExit("derived/ is stale at this commit: " + ", ".join(stale + extra))
    dest = Path(out_root) / f"sesiidae-atlas-v{version}"
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "derived").mkdir(parents=True)
    (dest / "schemas").mkdir()
    contents = {}
    for name, data in files.items():
        contents[f"derived/{name}"] = data
    for p in sorted((ROOT / "schemas").glob("*.json")):
        contents[f"schemas/{p.name}"] = p.read_bytes()
    for name in BUNDLE_EXTRA:
        contents[name] = (ROOT / name).read_bytes()
    manifest = {"atlas_version": version, "tag": tag if tag in tags else None, "git_commit": commit,
                "commit_date": git("log", "-1", "--format=%cI", "HEAD"),
                "doi": None, "schema_version": SCHEMA_VERSION,
                "files_sha256": {n: sha256(d) for n, d in sorted(contents.items())}}
    contents["manifest.json"] = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode("utf-8")
    contents["SHA256SUMS"] = "".join(f"{sha256(contents[n])}  {n}\n" for n in sorted(contents)).encode("utf-8")
    for name, data in contents.items():
        (dest / name).parent.mkdir(parents=True, exist_ok=True)
        (dest / name).write_bytes(data)
    return dest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if derived/ differs from a fresh build")
    ap.add_argument("--bundle", metavar="VERSION", help="build dist/sesiidae-atlas-v<VERSION>/")
    ap.add_argument("--allow-untagged", action="store_true", help="bundle without a v<VERSION> tag (test bundles only)")
    ap.add_argument("--out", default=str(ROOT / "dist"), help="where bundles go")
    args = ap.parse_args(argv)
    if args.bundle:
        dest = bundle(args.bundle, args.allow_untagged, args.out)
        print(f"wrote {dest}")
        return 0
    files = derived_files(ROOT / "data")
    if args.check:
        stale, extra = check_derived(files)
        if stale or extra:
            print("derived/ is stale: " + ", ".join(stale + [f"{e} (not built by this script)" for e in extra])
                  + "\nrun python scripts/build_release.py", file=sys.stderr)
            return 1
        print("derived/ is current")
        return 0
    write_derived(files)
    print("wrote derived/: " + ", ".join(sorted(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
