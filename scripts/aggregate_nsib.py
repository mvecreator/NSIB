#!/usr/bin/env python3
"""
Aggregate multiple NSIB-P1 model runs.

Expected directory layout:

runs/
  gpt56sol_r1.jsonl
  gpt56sol_r2.jsonl
  gemini_x_r1.jsonl
  ...

Each JSONL may optionally contain a metadata row first:
{"type":"meta","model":"GPT-5.6 Sol","provider":"OpenAI","run":"R1",
 "date":"2026-09-15","reasoning_mode":"high","temperature":null,"seed":null}

All other rows:
{"id":"P1-A01","output":"ANSWER: B\n..."}
For Family F:
{"id":"P1-F01","output":"...","constraint_scores":[1,1,1,1,1,1]}

Usage:
  python aggregate_nsib.py RUNS_DIR NSIB_P1_EVALUATOR_KEY.jsonl OUT_PREFIX

Outputs:
  OUT_PREFIX_runs.csv
  OUT_PREFIX_models.csv
  OUT_PREFIX_summary.json
"""

import sys, json, re, csv
from pathlib import Path
from collections import defaultdict
from statistics import mean, pstdev

def load_jsonl(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def extract_answer(text):
    m = re.search(r'(?im)^\s*ANSWER\s*:\s*([ABCD])\b', text or "")
    return m.group(1).upper() if m else None

def score_run(rows, keys):
    meta = {"model":"UNKNOWN","provider":"","run":"","date":"","reasoning_mode":"","temperature":None,"seed":None}
    data=[]
    for r in rows:
        if r.get("type")=="meta":
            meta.update({k:v for k,v in r.items() if k!="type"})
        else:
            data.append(r)

    answers={}
    fam_total=defaultdict(int)
    fam_correct=defaultdict(int)
    closed_total=closed_correct=0
    f_num=f_den=0
    unparsed=[]
    hallucinations=0

    for r in data:
        tid=r.get("id")
        if tid not in keys:
            continue
        k=keys[tid]
        fam=k["family"]
        if fam!="F":
            pred=extract_answer(r.get("output",""))
            answers[tid]=pred
            fam_total[fam]+=1
            closed_total+=1
            if pred==k["correct"]:
                fam_correct[fam]+=1
                closed_correct+=1
            if pred is None:
                unparsed.append(tid)
        else:
            scores=r.get("constraint_scores")
            expected=len(k["correct"]["hard_constraints"])
            if isinstance(scores,list) and len(scores)==expected and all(x in (0,1) for x in scores):
                f_num+=sum(scores)
                f_den+=len(scores)
        hallucinations += int(r.get("hallucinated_semantic_collapses",0) or 0)

    b_pairs=defaultdict(list)
    c_pairs=defaultdict(list)
    e_turns=defaultdict(list)
    for k in keys.values():
        if k["family"]=="B":
            b_pairs[k.get("pair_id")].append(k)
        elif k["family"]=="C":
            c_pairs[k.get("pair_id")].append(k)
        elif k["family"]=="E":
            e_turns[k.get("turn")].append(k)

    b_pair_seen=b_pair_ok=0
    for pid,pair in b_pairs.items():
        if pid is None:
            continue
        if all(x["id"] in answers and answers[x["id"]] is not None for x in pair):
            b_pair_seen+=1
            if all(answers[x["id"]]==x["correct"] for x in pair):
                b_pair_ok+=1

    c_pair_seen=c_pair_ok=0
    for pid,pair in c_pairs.items():
        if pid is None:
            continue
        if all(x["id"] in answers and answers[x["id"]] is not None for x in pair):
            c_pair_seen+=1
            preds=[answers[x["id"]] for x in pair]
            if len(set(preds))==1 and all(preds[i]==pair[i]["correct"] for i in range(len(pair))):
                c_pair_ok+=1

    e_by_turn={}
    for turn, items in sorted(e_turns.items()):
        seen=correct=0
        for k in items:
            if k["id"] in answers and answers[k["id"]] is not None:
                seen+=1
                correct += answers[k["id"]]==k["correct"]
        e_by_turn[f"E_turn_{turn}_acc"] = (correct/seen if seen else None)

    acc=closed_correct/closed_total if closed_total else None
    f_cons=f_num/f_den if f_den else None
    aggregate = 100*(0.85*acc + 0.15*f_cons) if acc is not None and f_cons is not None else None

    result={
        **meta,
        "closed_accuracy":acc,
        "A_acc": fam_correct["A"]/fam_total["A"] if fam_total["A"] else None,
        "B_acc": fam_correct["B"]/fam_total["B"] if fam_total["B"] else None,
        "C_acc": fam_correct["C"]/fam_total["C"] if fam_total["C"] else None,
        "D_acc": fam_correct["D"]/fam_total["D"] if fam_total["D"] else None,
        "E_acc": fam_correct["E"]/fam_total["E"] if fam_total["E"] else None,
        "B_pair_sensitivity": b_pair_ok/b_pair_seen if b_pair_seen else None,
        "C_isomorphism_correct_consistency": c_pair_ok/c_pair_seen if c_pair_seen else None,
        "F_conservation":f_cons,
        "NSIB_P1":aggregate,
        "H_semantic_collapse":hallucinations,
        "closed_scored":closed_total,
        "F_constraints_scored":f_den,
        "unparsed_count":len(unparsed),
    }
    result.update(e_by_turn)
    return result

def avg(vals):
    vals=[v for v in vals if isinstance(v,(int,float))]
    return mean(vals) if vals else None

def sd(vals):
    vals=[v for v in vals if isinstance(v,(int,float))]
    return pstdev(vals) if len(vals)>1 else 0.0 if vals else None

def main():
    if len(sys.argv)!=4:
        raise SystemExit("Usage: python aggregate_nsib.py RUNS_DIR KEY.jsonl OUT_PREFIX")

    runs_dir=Path(sys.argv[1])
    key_path=Path(sys.argv[2])
    out_prefix=Path(sys.argv[3])

    keys={r["id"]:r for r in load_jsonl(key_path)}
    run_rows=[]
    for p in sorted(runs_dir.glob("*.jsonl")):
        rr=score_run(load_jsonl(p),keys)
        rr["source_file"]=p.name
        run_rows.append(rr)

    if not run_rows:
        raise SystemExit("No .jsonl run files found.")

    grouped=defaultdict(list)
    for r in run_rows:
        grouped[r["model"]].append(r)

    metric_cols=[
        "closed_accuracy","A_acc","B_acc","C_acc","D_acc","E_acc",
        "B_pair_sensitivity","C_isomorphism_correct_consistency",
        "F_conservation","NSIB_P1","H_semantic_collapse",
        "E_turn_1_acc","E_turn_2_acc","E_turn_3_acc","E_turn_4_acc","E_turn_5_acc"
    ]

    model_rows=[]
    for model, rows in grouped.items():
        mr={"model":model,"n_runs":len(rows)}
        for col in metric_cols:
            vals=[r.get(col) for r in rows]
            mr[col+"_mean"]=avg(vals)
            mr[col+"_sd"]=sd(vals)
        model_rows.append(mr)

    ranked=sorted(
        model_rows,
        key=lambda x: (x.get("NSIB_P1_mean") is not None, x.get("NSIB_P1_mean") or -1),
        reverse=True
    )
    for i,r in enumerate(ranked,1):
        r["rank"]=i

    def write_csv(path, rows):
        cols=[]
        for r in rows:
            for k in r:
                if k not in cols:
                    cols.append(k)
        with open(path,"w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

    write_csv(str(out_prefix)+"_runs.csv", run_rows)
    write_csv(str(out_prefix)+"_models.csv", ranked)

    summary={
        "n_models":len(grouped),
        "n_runs":len(run_rows),
        "ranking": ranked,
        "runs": run_rows
    }
    Path(str(out_prefix)+"_summary.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"
    )

    print(json.dumps({
        "models":len(grouped),
        "runs":len(run_rows),
        "top_model": ranked[0]["model"] if ranked else None,
        "outputs":[
            str(out_prefix)+"_runs.csv",
            str(out_prefix)+"_models.csv",
            str(out_prefix)+"_summary.json"
        ]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
