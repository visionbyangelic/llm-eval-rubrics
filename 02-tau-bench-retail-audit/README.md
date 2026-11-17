# Sample 02: Auditing real agent runs and answer keys (tau-bench retail)

A review of **real** shopping-agent tasks and **real** model runs from the public tau-bench benchmark (Sierra Research, MIT licence): https://github.com/sierra-research/tau-bench. The tasks are customer-service orders on a retail site: cancel, modify, return, exchange. The agent is graded against a ground-truth key, which is the same kind of object as a rubric.

Everything below was run by me on the repo's own files. `verify.py` reproduces every number. I reviewed **two tasks in depth**, one that needs a fix and one that is fair, and say plainly what I did not review.

## How the benchmark scores a run

From `tau_bench/envs/base.py` (`calculate_reward`):
1. The task's ground-truth actions are replayed on a fresh database. The agent's final database must hash-match the result.
2. If the task lists expected `outputs`, each must appear as a substring in one of the agent's replies (case-insensitive, commas removed). Otherwise reward is 0.
3. Failed tool calls during replay are caught and turned into an `"Error: ..."` message instead of stopping.

Point 3 matters in Case 1.

## Scoreboard (Sonnet 3.5 new, retail, 115 tasks × 8 trials = 920 runs)

637 passed, 283 failed. Seven tasks were never passed in any trial: 34, 41, 66, 79, 92, 99, 104. Tasks 34, 41, 79 and 99 were also never passed by the GPT-4o runs in the same repo (4 trials each). Tasks that nothing passes are the best place to look for a bad key, so I started there.

| Task | My call | One-line reason |
|---|---|---|
| 34 | **FIX** | Key replays with an error; one required output is unreachable on the key's own path |
| 79 | **KEEP** | Failure is fair; one hardening note |
| 41, 66, 92, 99, 104 | not reviewed | |

---

## Case 1: Task 34, "Noah Patel", the key that errors silently

**Instruction (condensed):** Noah ordered office items and hiking gear for a Seattle move. If **cancelling partial items is possible**, he wants to return the office items, keep the hiking items, learn the total refund, and have it go to the original payment method. **If not possible**, he just wants the order's address changed to his NYC address.

**Key as stored in the trajectory files:** one write action, `modify_pending_order_address` on `#W1845024`, and one required output, `"1093.34"`.

### Finding 1: the key's only write action fails when replayed
- The key's kwargs use `province`. The tool's signature takes `state`. Across all **115** embedded keys, this is the **only** action whose kwargs don't match its tool's signature.
- Replaying the key against the real tool code gives `got an unexpected keyword argument 'province'`. Because the benchmark turns tool errors into a string, the key silently does nothing, and the **expected final state is the untouched database** (verified by hash).
- The agent did what the instruction's "not possible" branch asks: it changed the address. That makes its database differ from the expected state, so it scores 0.
- With `province` changed to `state`, the agent's state **matches** the key (verified by hash).
- The current `tasks_test.py` in the repo already uses `state` for this task, so the key appears to have been fixed upstream. The saved trajectory files still carry the old key. I only cloned the latest commit, so I can't say when it was fixed.

### Finding 2: the required output is unreachable on the key's own path
- `1093.34` is checkable: the three office items in the order are $235.13 + $346.97 + $511.24 = **$1,093.34**.
- But the cancel tool takes only an order and a reason (`invoke(data, order_id, reason)`), so partial cancellation isn't possible. The key's actions contain no cancellation, so no refund exists on the key's path. The user only wants the refund total in the branch the policy rules out.
- Result: **0 of 8** Sonnet runs state the total, and the benchmark scored all 4 GPT-4o runs 0 on this output as well. The current upstream file still requires it.
- A fair agent has no reason to say it: nothing in the "not possible" branch asks for it, and a simulated user in that branch has no reason to ask.

### Call: FIX
- *Information available?* Yes. Prices are in the order details.
- *Key matches the instruction?* No. Finding 1 is a key bug. Finding 2 is a leftover from the branch that can't happen.
- *Valid answer marked wrong?* Yes. The correct behaviour (explain that partial cancellation isn't possible, change the address, confirm) is scored 0.
- *Fix:* (a) keep `state` in the key, and (b) delete the `1093.34` output, or rewrite the task so the refund question is asked on the path the key follows (for example, a full cancellation with a stated refund).

**Note:** The agent behaved correctly. Two defects in the key, one a wrong kwarg that voids the expected state and one an output tied to an impossible branch, make this task unwinnable. Re-scoring is not possible without the fix, so I would not count these 12 failures as model errors.

---

## Case 2: Task 79, "Emma Kovacs", the failure that is fair

**Instruction (condensed):** She regrets her **500 ml** water bottle and wants to change it to "the other bottle you just placed with **1000 ml** capacity." If the exact item is unavailable, she can allow **the material** to be different.

**Key:** change item `3453331371` (500 ml, stainless steel, black) in `#W8661412` to `2439754078`.

### What the data says (checked in `products.json` and `orders.json`)
- "The other bottle" is `1434748144` in order `#W9284598`: **1000 ml, glass, red**, $49.72, and `available: False`.
- The key's target `2439754078` is **1000 ml, stainless steel, red**, $49.51, available. Same capacity and colour as the user's bottle; only the material differs, which is exactly the one deviation the instruction permits.
- All 8 Sonnet runs chose `7661609223`: 1000 ml, stainless steel, **black**, $46.51, available. It matches the bottle being *replaced* (material and colour) instead of the bottle being *wanted*.

### Where the agent went wrong
In trial 0 the agent read both orders, listed both bottles correctly, and asked what options she preferred. It then proposed the black stainless version on the grounds that it matched the current bottle's material, without checking colour. The agent changed the colour, which the instruction does not allow.

### Call: KEEP
- *Information available?* Yes. Colour, material and availability of the target were in the order data the agent had already read.
- *Key matches the instruction?* Yes. The target is the only available item that keeps the wanted bottle's capacity and colour and varies only the material.
- *Valid answer marked wrong?* No. The black bottle isn't the stated target and changes an attribute the instruction didn't release.
- *Hardening note (not a fix):* the instruction never tells the simulated user to refuse a different colour, and in trial 0 the user accepted black ("Yes, that sounds good"). Adding "you want it red and would decline other colours" would remove the dependence on the simulator's mood.

**Note:** Fair failure. The agent copied the wrong bottle's attributes and the simulated user didn't catch it. Key is correct; I would only tighten the user script.

---

## What I did not do
- I reviewed 2 of the 7 never-passed tasks. Tasks 41, 66, 92, 99 and 104 are unreviewed; I only saw that in 41 and 99 the agents' write actions differ from the key, and did not audit why.
- I read one trial fully for each case. The other trials' write actions and scores were checked by script, not read line by line.
- Only the Sonnet 3.5 and GPT-4o retail trajectories were used. I didn't run any model.

## Reproduce
```
git clone --depth 1 https://github.com/sierra-research/tau-bench.git
pip install pydantic
python3 verify.py ./tau-bench
```
