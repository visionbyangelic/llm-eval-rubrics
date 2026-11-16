"""Audit of GSM8K test-set reference solutions (public data, MIT licence).

Source: https://github.com/openai/grade-school-math  (grade_school_math/data/test.jsonl)
Run:    curl -L -o test.jsonl https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl
        python3 audit.py
"""
import json, re

rows = [json.loads(l) for l in open("test.jsonl")]

def evaluate(expr):
    e = expr.replace(",", "")
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\) ]+", e):
        return None
    try:
        return eval(e)
    except Exception:
        return None

bad_calc, final_mismatch = [], []
for i, r in enumerate(rows):
    ans = r["answer"]
    final = float(ans.split("####")[-1].strip().replace(",", ""))
    last = None
    for expr, res in re.findall(r"<<(.*?)=(.*?)>>", ans):
        try:
            stated = float(res.replace(",", ""))
        except ValueError:
            continue
        v = evaluate(expr)
        if v is not None and abs(v - stated) > 0.011:
            bad_calc.append((i, expr, res, v))   # check 1: annotation arithmetic
        last = stated
    if last is not None and abs(final - last) > 1e-6:
        final_mismatch.append((i, final, last))  # check 2: final vs last annotated step

print("rows:", len(rows))
print("check 1, annotation arithmetic mismatches:", len(bad_calc))
print("check 2, final answer != last annotated result:", len(final_mismatch))
print("check 3, item 255:", rows[255]["question"])
