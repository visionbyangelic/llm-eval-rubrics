"""Re-checks the two findings in README.md against the public tau-bench repo.

Setup:
    git clone --depth 1 https://github.com/sierra-research/tau-bench.git
    pip install pydantic
    python3 verify.py ./tau-bench
(litellm is stubbed because nothing here calls an LLM.)
"""
import sys, types, json, inspect, copy, collections

root = sys.argv[1] if len(sys.argv) > 1 else "./tau-bench"
sys.modules["litellm"] = types.SimpleNamespace(completion=None, completion_cost=None)
sys.path.insert(0, root)
from tau_bench.envs.retail.tools import ALL_TOOLS
from tau_bench.envs.retail.data import load_data
from tau_bench.envs.base import consistent_hash, to_hashable

tools = {T.get_info()["function"]["name"]: T for T in ALL_TOOLS}
sig = {n: [p for p in inspect.signature(T.invoke).parameters if p != "data"] for n, T in tools.items()}
runs = json.load(open(f"{root}/historical_trajectories/sonnet-35-new-retail.json"))
tasks = {r["task_id"]: r["info"]["task"] for r in runs if r["trial"] == 0}

print("== Scoreboard")
print("runs:", len(runs), "| passed:", sum(r["reward"] == 1 for r in runs), "| failed:", sum(r["reward"] == 0 for r in runs))
by = collections.defaultdict(list)
for r in runs: by[r["task_id"]].append(r["reward"])
print("tasks never passed (Sonnet 3.5 new, 8 trials each):", sorted(t for t, v in by.items() if sum(v) == 0))

print("\n== Check A: ground-truth actions whose kwargs do not match the tool signature")
bad = []
for tid, t in sorted(tasks.items()):
    for a in t["actions"]:
        if a["name"] in sig:
            extra = sorted(set(a["kwargs"]) - set(sig[a["name"]]))
            missing = sorted(set(sig[a["name"]]) - set(a["kwargs"]))
            if extra or missing: bad.append((tid, a["name"], extra, missing))
print("tasks checked:", len(tasks), "| mismatches:", len(bad))
for b in bad: print("  task", b[0], b[1], "unexpected:", b[2], "missing:", b[3])

print("\n== Check B: replay task 34's ground truth against the real tools and data")
def replay(actions):
    data = copy.deepcopy(load_data()); errs = []
    for a in actions:
        if a["name"] in ("think", "transfer_to_human_agents"): continue
        try: tools[a["name"]].invoke(data=data, **a["kwargs"])
        except Exception as e: errs.append((a["name"], str(e)[:90]))
    return consistent_hash(to_hashable(data)), errs
t = tasks[34]
gt_hash, gt_err = replay(t["actions"]); base_hash, _ = replay([])
agent = [{"name": "modify_pending_order_address", "kwargs": {"order_id": "#W1845024", "address1": "224 Elm Street", "address2": "Suite 491", "city": "New York", "state": "NY", "country": "USA", "zip": "10108"}}]
agent_hash, _ = replay(agent)
fixed = copy.deepcopy(t["actions"])
for a in fixed:
    if a["name"] == "modify_pending_order_address" and "province" in a["kwargs"]:
        a["kwargs"]["state"] = a["kwargs"].pop("province")
fixed_hash, fixed_err = replay(fixed)
print("ground-truth errors as embedded:", gt_err)
print("expected final state == untouched database:", gt_hash == base_hash)
print("agent's address change == expected state (as embedded):", agent_hash == gt_hash)
print("after province->state fix: errors", fixed_err, "| agent state == expected:", agent_hash == fixed_hash)

print("\n== Check C: where 1093.34 comes from (order #W1845024)")
orders = load_data()["orders"]
office = [i for i in orders["#W1845024"]["items"] if i["name"] in ("Mechanical Keyboard", "Headphones", "Office Chair")]
print([(i["name"], i["price"]) for i in office], "sum =", round(sum(i["price"] for i in office), 2))
said = sum(any("1093" in str(m.get("content")) for m in r["traj"] if m["role"] == "assistant") for r in runs if r["task_id"] == 34)
print("Sonnet trials (of 8) in which the agent states the total:", said)
