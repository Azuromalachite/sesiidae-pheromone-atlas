"""Motivating observations for espmap-sesiidae-001, rule direct_contrast_v1.

An observation motivates a contrast if it directly compares the contrast's
two members:
  (a) an electrophysiology record whose responses include both members; or
  (b) a field-trapping record whose treatment and comparator blends differ
      ONLY in the two members (presence or amount), with the same trap and
      dispenser, and with both members present in the pair of blends.
Every effect and significance is kept as recorded.

The frozen lists in case-bundle.yaml were made at Atlas e8ca212 (atlas_pin).
To reproduce them, run this at that commit; on a later commit the list may
grow as records are added, which does not change the frozen study.

    python analyses/espmap-sesiidae-001/motivating.py            # ID lists, as in case-bundle.yaml
    python analyses/espmap-sesiidae-001/motivating.py --detail   # with taxon, effect and significance
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import atlas_validate as av  # noqa: E402

C = lambda s: f"spa.cmpd.{s}"
PAIRS = {"B_stereo": (C("z3_z13_18_oac"), C("e3_z13_18_oac")), "C_position": (C("e3_z13_18_oac"), C("e2_z13_18_oac"))}


def amounts(blend):
    return {b["compound"]: json.dumps(b.get("amount"), sort_keys=True) for b in blend or []}


def motivating(obs, pair):
    pair = set(pair)
    out = []
    for oid, o in obs.items():
        if o["observation_type"] == "electrophysiology" and pair <= {r["compound"] for r in o["responses"]}:
            out.append(oid)
        elif o["observation_type"] == "behavioural_response" and o.get("assay") == "field_trapping" and (o.get("comparator") or {}).get("blend"):
            comp = o["comparator"]
            if "trap" in comp or "dispenser" in comp:
                continue
            t, c = amounts(o["blend"]), amounts(comp["blend"])
            diff = {k for k in set(t) | set(c) if t.get(k) != c.get(k)}
            if diff and diff <= pair and pair <= set(t) | set(c):
                out.append(oid)
    return sorted(out)


def main(argv=None):
    detail = "--detail" in (argv if argv is not None else sys.argv[1:])
    records, findings = av.load_root(ROOT / "data")
    if findings:
        raise SystemExit("records do not load; run atlas_validate.py first")
    obs = {k: v[1] for k, v in records["observations"].items()}
    for name, pair in PAIRS.items():
        ids = motivating(obs, pair)
        print(f"{name}:  # {len(ids)} observations in {len({obs[i]['taxon'] for i in ids})} taxa")
        for oid in ids:
            o = obs[oid]
            extra = f"  # {o.get('effect', 'electrophysiology')}, {o.get('significance', '-')}" if detail else ""
            print(f"  - {oid}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
