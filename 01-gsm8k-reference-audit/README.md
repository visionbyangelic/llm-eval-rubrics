# Sample 01: Auditing the reference answers of a public benchmark (GSM8K)
 
A review of the reference ("gold") answers in a real, public LLM benchmark. The question I'm asking is the one I'd ask of any task someone else drafted: **can I trust the answer key, and would a correct model answer be marked wrong?**
 
**This sample uses real data.** The data is the GSM8K test set (1,319 grade-school math word problems with reference solutions) from OpenAI's public repository, MIT-licensed: https://github.com/openai/grade-school-math. Everything below was run by me on that file. `audit.py` reproduces the numbers.
 
## Context (from published work, not my finding)
 
GSM8K is known to contain label noise. The paper *Do Large Language Model Benchmarks Test Reliability?* (Vendrow et al., 2025, arXiv:2502.03461) re-checked the GSM8K test set and released GSM8K-Platinum. By the dataset card: of 1,319 test questions, 219 were flagged by models, of which 110 were rejected, 10 were re-labeled and 99 were verified as correct, leaving 1,209. The paper groups bad questions into logical contradictions, ambiguity, and flawed construction. I did not retrieve their rejected-item list, so I can't say which items I checked appear in it, apart from the one the paper shows as an example (Check 3).
 
## What I checked
 
### Check 1: Do the reference solutions' arithmetic annotations hold?
Each reference solution embeds calculator annotations like `<<9*2=18>>`. I recomputed every one.
**Result: 0 mismatches in 1,319 solutions.** The calculator steps themselves are clean, so any label noise is not simple arithmetic slips inside annotated steps.
 
### Check 2: Does the final answer match the last annotated result?
A mismatch could signal a wrong final line.
**Result: 93 items differ.** I read the first eight by hand (indexes 13, 14, 29, 34, 43, 81, 98, 107) and solved each independently. **All eight reference answers are correct.** In every one, the last step (converting to a percentage, adding $5, subtracting, an unannotated "2 fewer") was simply written without a calculator annotation.
**Call: this check is too noisy to use as an error detector.** It would flood a reviewer with false positives. I have not reviewed the other 85, so I make no claim about them. A reviewer using this check should treat it as a prompt to read, not as evidence of an error.
 
### Check 3: Read a documented problem item directly
Item at index 255 (line 256 of `test.jsonl`):
 
> Ten stalls have 20 cows each. Mr. Sylas buys 40 cows and divides them equally, putting an equal number of the new cows into each of the twenty stalls. How many cows are in 8 of the stalls?
 
Reference answer: **192**, using 40 ÷ 10 = 4 new cows per stall, then 8 × (20 + 4) = 192.
 
My review:
- *Information available?* The prompt contradicts itself: it says there are **ten** stalls, then says the new cows go into each of the **twenty** stalls.
- *Which reading does the key use?* Ten. Under "twenty stalls" the cows would split 40 ÷ 20 = 2 per stall, and the answer would also depend on how many cows are in the ten stalls the prompt never describes (no count is given for them), so it is not computable.
- *Would a valid answer be marked wrong?* A model that follows the second sentence literally and answers from a twenty-stall setup would be marked wrong, although the prompt supports that reading.
- **Call: REJECT (task can't be saved by changing the key).** Fixing the key to 192 or to any other number just picks one of two readings. The prompt itself needs a correction. This matches the paper's example of a logical-contradiction question.
I found this item in the raw data and checked the contradiction and both readings myself. I was pointed to it by the published paper, not by my own search.
 
## What this shows about how I review
 
- I run a mechanical check first, report the result **even when it is negative** (Check 1), and don't oversell weak signals (Check 2).
- I verify flagged items by solving them independently instead of trusting either the key or the flag.
- When a task is internally inconsistent, I reject it and say why, instead of "fixing" the answer.
## Limits
 
- I reviewed 8 of the 93 items from Check 2 and one item from the literature. I make no claim about the rest of the dataset.
- I did not re-derive GSM8K-Platinum's 110 rejections or 10 re-labels.
- No model was run here; this is an audit of the answer key, not of any model.
## Reproduce
 
```
curl -L -o test.jsonl https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl
python3 audit.py
```
 
