#!/usr/bin/env python3
"""Score one NSIB run against a separately supplied evaluator key."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

def load(path):
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]

def ans(text):
    m=re.search(r"(?im)^\s*ANSWER\s*:\s*([ABCD])\b", text or "")
    return m.group(1).upper() if m else None

if len(sys.argv)!=3:
    raise SystemExit("Usage: python score_run.py RUN.jsonl KEY.jsonl")

rows=load(sys.argv[1])
keys={x["id"]:x for x in load(sys.argv[2])}
tot=ok=0
byfam=defaultdict(lambda:[0,0])

for r in rows:
    if r.get("type")=="meta" or r.get("id") not in keys:
        continue
    k=keys[r["id"]]
    if k.get("family")=="F":
        continue
    pred=ans(r.get("output",""))
    tot+=1
    byfam[k["family"]][1]+=1
    if pred==k["correct"]:
        ok+=1
        byfam[k["family"]][0]+=1

print(json.dumps({
    "closed_accuracy": ok/tot if tot else None,
    "closed_correct": ok,
    "closed_total": tot,
    "family_accuracy": {
        f: c/t if t else None for f,(c,t) in sorted(byfam.items())
    }
}, ensure_ascii=False, indent=2))
