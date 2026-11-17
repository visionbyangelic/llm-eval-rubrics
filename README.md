# llm-eval-rubrics

Work samples in reviewing LLM evaluation material: checking answer keys and rubrics, reading agent transcripts for the point where they go wrong, and deciding whether a failure is fair. Each sample ends in a short written call (KEEP, FIX or FLAG) and says what I did not check.

| Sample | Data | What it shows |
|---|---|---|
| [01-gsm8k-reference-audit](01-gsm8k-reference-audit) | **Real.** GSM8K test set (public, MIT) | Mechanical checks on an answer key, including a negative result; a contradictory problem rejected |
| [02-tau-bench-retail-audit](02-tau-bench-retail-audit) | **Real.** tau-bench retail tasks and model runs (public, MIT) | A key that silently fails on replay, an output no fair agent would state, and a failure that is fair |
| [03-shopping-delivery-synthetic](03-shopping-delivery-synthetic) | **Synthetic.** Written by me, labelled as such | Five worked cases in the shopping/delivery rubric-review format |

Samples 01 and 02 come with scripts that reproduce every number from the public sources. Sample 03 is made up on purpose, to show the method on cases where I control the answer.

## How I review
1. Was the information available to the agent?
2. Does the rubric grade what the prompt asked, and nothing it didn't?
3. Would a valid answer have been marked wrong?
4. Is the rubric well-formed: atomic criteria, outcome over process, checkable by two reviewers?

I recompute numbers and replay keys myself instead of trusting a reference answer, and I report negative results and unreviewed items.

No confidential, client or employer material is used anywhere in this repository.
