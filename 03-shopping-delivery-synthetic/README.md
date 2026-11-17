# LLM Eval Rubric Review: Shopping & Delivery Agent Tasks

A work sample showing how I review AI-drafted agent tasks. Each case has a prompt, a grading rubric, an environment snapshot and a model attempt. For each one I decide whether the failure is fair, fix the criteria that aren't, flag the tasks that can't be saved, and write a short note on the call.

> **Read this first.** All tasks, stores, products, prices and transcripts here are **synthetic**, written by me for this sample. They are not from any employer, client, platform or real project, and no confidential material is used. The rubric conventions below are my own working assumptions, since I haven't seen any project's guidelines; I would adapt them to the real ones on day one.

---

## Summary of calls

| # | Task | Model result | My call | What changed |
|---|------|--------------|---------|--------------|
| 1 | Pancake ingredients under $20 | Picked a non-maple syrup | **KEEP.** Failure is fair | Nothing |
| 2 | Pizza delivery before 7:30 pm | Chose Priority delivery | **FIX.** Valid answer marked wrong | Criterion C4 rewritten |
| 3 | Lowest price per 100 ml detergent | Chose PureWash | **FIX.** Reference answer is wrong | D1–D3 corrected |
| 4 | Reorder "my usual" to "my work address" | Guessed item and address | **FLAG.** Can't be saved | Inputs don't exist anywhere the agent can see |
| 5 | Pasta order with total reported | Chose a different valid sauce | **FIX.** Rubric structure | Compound criterion split; process and vague criteria removed |

---

## How I review a case

For every task I answer four questions, in this order, using only what the prompt and environment actually contain:

1. **Was the information available?** Could the agent have found every fact the rubric depends on, in the prompt or in the environment (listing text, product page, cart, order history, saved addresses)?
2. **Does the rubric grade what the prompt asked?** Every criterion must trace to a sentence in the prompt. If the rubric asks for something the prompt never asked, it is over-specified. If the prompt asked for something the rubric never checks, it is under-specified.
3. **Would a valid answer have been marked wrong?** I list every answer that satisfies the prompt, then check each against the rubric.
4. **Is the structure sound?** (see conventions below)

I also **recompute every number and re-read every product listing myself.** I do not trust the reference answer. In Case 3 the reference answer was wrong.

### Rubric conventions I applied

- **One criterion, one check.** No "and" chains that bundle several checks into one pass/fail.
- **Outcome over process.** Grade the final cart, order, or reply, not whether the agent "carefully compared" things, unless the prompt asked for a specific process.
- **Objectively verifiable.** Two reviewers should reach the same pass/fail from the transcript. Words like "clear", "professional" or "carefully" are not checkable.
- **Accept every valid path.** If the prompt allows several correct answers, the criterion names the rule, not one example.
- **Dependent values are relative.** A total should be checked against the agent's own final cart, so one wrong choice is penalised once, not twice.
- **No hidden information.** A criterion cannot rely on facts that exist only in the drafter's head.
- **Weights track importance.** Core outcomes carry more points than formatting or reporting.

### Decision labels

- **KEEP**: the failure is fair; the rubric grades what the prompt asked.
- **FIX**: the task is sound but one or more criteria are wrong; I rewrite them.
- **FLAG**: the task can't be saved by editing criteria; I explain why.

---

## Case 1: FreshCart pancake ingredients

**Prompt**
> I'm making pancakes for four. On FreshCart, add to my cart: one 12-count carton of eggs, one 1 kg bag of plain flour, 1 L of whole milk, and the cheapest real maple syrup that comes in at least 250 ml. Nothing else. Keep the items total under $20 and tell me the total.

**Environment (relevant listings)**

| Product | Size | Price | Listing note |
|---|---|---|---|
| Eggs | 12-count | $3.49 | |
| Plain flour | 1 kg | $1.99 | |
| Whole milk | 1 L | $1.59 | |
| Maple Grove Pure Maple Syrup | 180 ml | $4.29 | |
| Pancake Style Syrup | 250 ml | $2.99 | *Maple-flavoured table syrup, 0% maple* |
| Vermont Gold Pure Maple Syrup | 250 ml | $6.49 | |
| Sugar Hill Pure Maple Syrup | 355 ml | $7.99 | |

**My answer key:** the only real maple syrups of at least 250 ml are Vermont Gold ($6.49) and Sugar Hill ($7.99). The cheapest is Vermont Gold. Total: 3.49 + 1.99 + 1.59 + 6.49 = **$13.56**.

**Rubric (as drafted)**

| ID | Criterion | Pts |
|---|---|---|
| R1 | Cart contains exactly one 12-count carton of eggs | 1 |
| R2 | Cart contains exactly one 1 kg plain flour | 1 |
| R3 | Cart contains exactly one 1 L whole milk (not semi-skimmed) | 1 |
| R4 | Syrup in cart is Vermont Gold Pure Maple Syrup 250 ml | 2 |
| R5 | No other items in the cart | 1 |
| R6 | Final reply states a total equal to the sum of the items in the final cart | 1 |
| R7 | Cart items total is under $20 | 1 |

**Model attempt (condensed transcript)**

1. Search "eggs 12" → adds Eggs 12-count, $3.49.
2. Search "plain flour 1kg" → adds Plain flour 1 kg, $1.99.
3. Search "whole milk 1L" → adds Whole milk 1 L, $1.59.
4. Search "maple syrup" → results show four syrups with sizes, prices and subtitles. The Pancake Style Syrup subtitle reads *Maple-flavoured table syrup, 0% maple*.
5. Agent reasoning: "Filtering to ≥250 ml and sorting by price, Pancake Style Syrup at $2.99 is cheapest." It does not open any product page.
6. Adds Pancake Style Syrup 250 ml, $2.99.
7. Views cart: 4 items, $10.06.
8. Final reply: "Added everything. Your total is $10.06, well under $20."

**Where it went wrong:** Steps 4–5. The agent filtered on size and price but ignored the word "real" in the prompt, and the disqualifying text was visible in the step 4 listing.

**Score:** R1, R2, R3, R5, R6, R7 pass; R4 fails → 6/8.

**Call: KEEP (failure is fair).**
- *Information available?* Yes. The disqualifying subtitle was in the search results themselves.
- *Rubric matches prompt?* Yes. "Real maple syrup" is in the prompt, and R4 grades exactly that.
- *Valid answer marked wrong?* Sugar Hill is also real maple ≥250 ml but not the cheapest, so rejecting it is correct.
- *Structure?* R6 is already defined relative to the agent's own cart, so the wrong syrup is penalised once (R4), not twice. The $10.06 total is arithmetically correct for the cart it built and rightly passes R6.

**Note:** No change needed. The agent skipped the "real maple" constraint despite visible evidence. Good example of a task that should be left alone.

---

## Case 2: QuickBite delivery deadline

**Prompt**
> Order a large margherita pizza and a 2 L cola from Luigi's on QuickBite for delivery to 14 Elm Street. It has to arrive before 7:30 pm tonight. Pay with my saved card.

**Environment:** current time 6:40 pm. Items: Large Margherita $12.50, Cola 2 L $3.00. Checkout delivery options:

| Option | Estimate | Arrival window | Fee |
|---|---|---|---|
| Standard | 35–45 min | 7:15–7:25 pm | $1.99 |
| Priority | 20–25 min | 7:00–7:05 pm | $4.98 |
| Schedule | pick a time, 7:00–9:00 pm, 15-min steps | chosen time | $1.99 |

**Rubric (as drafted)**

| ID | Criterion | Pts |
|---|---|---|
| C1 | Cart has 1 × large margherita from Luigi's | 2 |
| C2 | Cart has 1 × 2 L cola | 1 |
| C3 | Delivery address is 14 Elm Street | 1 |
| C4 | Agent selects the **Standard** delivery option | 3 |
| C5 | Payment method is the saved card | 1 |
| C6 | Order is placed (confirmation page reached) | 1 |

**Model attempt (condensed transcript)**

1. Opens Luigi's menu; adds Large Margherita and Cola 2 L.
2. Goes to checkout; address field pre-filled with a different saved address; changes it to 14 Elm Street.
3. Reads delivery options and the clock (6:40 pm).
4. Reasoning: "Standard arrives 7:15–7:25, which technically meets the deadline, but Priority gives more margin for a hard deadline." Selects **Priority**.
5. Selects saved card; places order.
6. Confirmation: total $20.48, ETA 7:00–7:05 pm.

**Where it went wrong:** nowhere. Every prompt requirement is met.

**Score:** C1, C2, C3, C5, C6 pass; C4 fails → 6/9.

**Call: FIX (valid answer marked wrong).**
- *Information available?* Yes, all of it.
- *Rubric matches prompt?* No. The prompt sets a deadline ("before 7:30 pm"), not a cost preference. C4 turns the drafter's unstated "cheapest option that meets the deadline" into a requirement.
- *Valid answer marked wrong?* Yes. Priority (arrives 7:00–7:05), and a scheduled slot of 7:00, 7:15 or earlier would all satisfy the prompt. Standard also satisfies it (window ends 7:25), but it is not the only valid choice.
- *Structure?* A single named option is over-specified for a constraint-based prompt.

**Revised criterion**

| ID | Criterion | Pts |
|---|---|---|
| C4 | Selected delivery option's estimated arrival window **ends before 7:30 pm** (Standard, Priority, or a scheduled time before 7:30 pm all qualify) | 3 |

**Note:** The agent made a defensible choice that fully meets the prompt. The rubric encoded an unstated cost preference, so the failure was unfair. If the task really is about cost, the right fix is to change the prompt ("choose the cheapest option that still arrives before 7:30"), but that changes the task, so I would only do it with the drafter's agreement. Revised score: 9/9.

---

## Case 3: HomeMart price per 100 ml

**Prompt**
> On HomeMart, compare the three liquid laundry detergents on the Laundry Essentials page and add the one with the lowest price per 100 ml to my cart (quantity 1). Tell me which one you picked and its price per 100 ml.

**Environment (Laundry Essentials page)**

| Product | Size | Price |
|---|---|---|
| Brightly Fresh Linen | 1.5 L | $9.60 |
| Suds & Co Ultra | 2 L | $12.40 |
| PureWash Sensitive | 900 ml | $5.40 |

**My recomputation**

| Product | Calculation | Per 100 ml |
|---|---|---|
| Brightly Fresh Linen | 9.60 ÷ 15 | $0.64 |
| Suds & Co Ultra | 12.40 ÷ 20 | $0.62 |
| PureWash Sensitive | 5.40 ÷ 9 | **$0.60** |

**Rubric (as drafted; reference answer: Suds & Co Ultra at $0.62/100 ml, with a drafter's note "largest bottle = best unit price")**

| ID | Criterion | Pts |
|---|---|---|
| D1 | Cart contains Suds & Co Ultra 2 L × 1 | 3 |
| D2 | Final reply names Suds & Co Ultra | 2 |
| D3 | Final reply states $0.62 per 100 ml | 1 |
| D4 | No other items in the cart | 1 |

**Model attempt (condensed transcript)**

1. Opens the Laundry Essentials page; reads the three listings.
2. Computes per-100 ml for each (0.64, 0.62, 0.60).
3. Adds PureWash Sensitive 900 ml × 1.
4. Final reply: "I picked PureWash Sensitive at $0.60 per 100 ml. Brightly Fresh Linen is $0.64 and Suds & Co Ultra is $0.62."

**Where it went wrong:** nowhere. Its arithmetic matches mine.

**Score as drafted:** D4 passes; D1–D3 fail → 1/7.

**Call: FIX (reference answer is wrong).**
- *Information available?* Yes, sizes and prices are on the page.
- *Rubric matches prompt?* The structure does, but the expected answer is factually wrong. The drafter assumed larger bottles are cheaper per ml. On this page the smallest bottle is the cheapest per ml.
- *Valid answer marked wrong?* The model's answer is the only correct one.
- *Structure?* Sound apart from the wrong value.

**Revised criteria**

| ID | Criterion | Pts |
|---|---|---|
| D1 | Cart contains PureWash Sensitive 900 ml × 1 | 3 |
| D2 | Final reply names PureWash Sensitive | 2 |
| D3 | Final reply states a price per 100 ml of $0.60 (accept 60¢ or $0.006 per ml) | 1 |
| D4 | No other items in the cart | 1 |

**Note:** Reference was wrong, not the model. Always put the arithmetic in the rubric so it can be checked (e.g. "5.40 ÷ 9 = 0.60"). Revised score: 7/7.

---

## Case 4: Green Bowl "my usual"

**Prompt**
> Reorder my usual from last week from Green Bowl, but swap the chicken for tofu, and have it delivered to my work address. Use the saved card.

**Environment**
- Order history page: *No past orders.*
- Saved addresses: Home, 8 Cedar Lane (only one).
- Saved payment: card ending 4417.
- Menu items with a chicken/tofu choice: **Harvest Bowl** and **Teriyaki Bowl**.

**Rubric (as drafted)**

| ID | Criterion | Pts |
|---|---|---|
| E1 | Cart contains Harvest Bowl with tofu (matching last week's order, chicken swapped) | 3 |
| E2 | Delivery address is 220 Marina Road (work) | 3 |
| E3 | Payment is the saved card | 1 |
| E4 | Order is placed | 1 |

**Model attempt (condensed transcript)**

1. Opens order history → "No past orders."
2. Opens saved addresses → only Home, 8 Cedar Lane.
3. Reasoning: "No history found. Two menu items offer chicken. I'll assume Harvest Bowl."
4. Adds Harvest Bowl with tofu.
5. Reasoning: "No work address saved; using home address."
6. Selects saved card; places order to 8 Cedar Lane.
7. Final reply: "Ordered a Harvest Bowl with tofu to your home address, since I couldn't find a work address."

**Where it went wrong:** Steps 1–3 are where the task breaks. Steps 3 and 5 are where the agent turns missing information into guesses and places a real order on them.

**Score as drafted:** E3, E4 pass → 2/8.

**Call: FLAG (can't be saved).**
- *Information available?* **No.** "My usual" and "my work address" exist only in the drafter's head. Order history is empty and no work address is saved. No agent could produce the rubric's expected cart or address from the environment.
- *Rubric matches prompt?* The rubric adds facts (Harvest Bowl, 220 Marina Road) that appear nowhere in the prompt or environment. Both are 3-point criteria.
- *Valid answer marked wrong?* Any answer is marked wrong, because the only correct approach (asking for the missing details) isn't graded at all.
- *Structure?* Fine, but irrelevant.

**Why it can't be fixed by editing criteria:** changing the rubric doesn't create the missing information. The task would have to be rewritten, either by putting the item and address in the prompt, or by redefining it as a clarification task.

**Note:** Flagged as unsalvageable. I would suggest to the drafter either (a) rewriting the prompt to name the item and address, which makes it a new task, or (b) if the guidelines allow clarification tasks, a rubric that rewards asking for the missing details and not placing the order. Separately, the agent placed a real order on guessed inputs. That is worth reporting as agent behaviour, but it doesn't make this rubric fair.

---

## Case 5: MarketMate pasta order

**Prompt**
> From MarketMate, order two 500 g packs of spaghetti and one jar of tomato sauce under $4 for delivery tomorrow between 8 and 10 am. Tell me the order total including delivery.

**Environment**

| Item | Size | Price |
|---|---|---|
| Spaghetti | 500 g | $1.79 each |
| Nonna's Classic tomato sauce | 400 g | $3.89 |
| Roma Select tomato sauce | 680 g | $4.49 |
| Basil & Co tomato sauce | 350 g | $2.99 |
| Delivery, tomorrow 8–10 am slot | | $3.50 |

**My answer key:** sauces under $4 are Nonna's ($3.89) and Basil & Co ($2.99). Roma Select ($4.49) does not qualify. Valid totals: with Nonna's, 3.58 + 3.89 + 3.50 = **$10.97**; with Basil & Co, 3.58 + 2.99 + 3.50 = **$10.07**.

**Rubric (as drafted)**

| ID | Criterion | Pts |
|---|---|---|
| F1 | The agent orders two 500 g spaghetti, one Nonna's Classic sauce, selects the 8–10 am slot tomorrow, and reports a total of $10.97 | 6 |
| F2 | The agent carefully compares all sauce options before choosing | 2 |
| F3 | The response is clear and professional | 1 |

**Model attempt (condensed transcript)**

1. Searches spaghetti; adds 2 × 500 g at $1.79.
2. Searches tomato sauce; reads all three jars and prices.
3. Reasoning: "Roma Select is $4.49, over the limit. Nonna's $3.89 and Basil & Co $2.99 both qualify; no preference given. Choosing Basil & Co."
4. Adds Basil & Co.
5. Checkout: selects tomorrow 8–10 am; fee $3.50.
6. Final reply: "Ordered 2 spaghetti and Basil & Co sauce for tomorrow 8–10 am. Total including delivery: $10.07."

**Where it went wrong:** nowhere. The order and the reported total are correct.

**Score as drafted:** F1 fails (0/6), F2 and F3 pass → 3/9.

**Call: FIX (rubric structure).**
- *Information available?* Yes.
- *Rubric matches prompt?* No. The prompt says "a jar of tomato sauce under $4", not Nonna's specifically. F1 hard-codes one valid brand and its total.
- *Valid answer marked wrong?* Yes. Basil & Co with a $10.07 total is fully correct.
- *Structure?* Three problems:
  1. **F1 is compound.** It bundles five checks (spaghetti, sauce, slot, total, brand) into one all-or-nothing criterion carrying 6 of 9 points.
  2. **F2 is a process criterion** ("carefully compares"). The prompt didn't ask for a comparison process, and "carefully" isn't objectively checkable.
  3. **F3 is unverifiable** ("clear and professional").

**Revised rubric**

| ID | Criterion | Pts |
|---|---|---|
| F1 | Cart has exactly 2 × spaghetti 500 g | 2 |
| F2 | Cart has exactly one tomato sauce priced under $4.00 (Nonna's $3.89 or Basil & Co $2.99; Roma Select $4.49 does not qualify) | 2 |
| F3 | Delivery slot is tomorrow, 8–10 am | 2 |
| F4 | Reply states a single total equal to the sum of the final cart plus the $3.50 delivery fee ($10.97 with Nonna's, $10.07 with Basil & Co) | 2 |
| F5 | No other items in the cart | 1 |

**Note:** The agent did everything right, but the original rubric would have scored it 3/9. Splitting F1 gives partial credit where it is due and removes the hard-coded brand. F2 and F3 are dropped because they were not checkable. Revised score: 9/9.

---

## Patterns across the five cases

- Most unfair failures come from **over-specified criteria**: a single valid path written into the rubric (Cases 2 and 5).
- **Unverified reference answers** are common and easy to catch. Re-do the arithmetic from the page (Case 3).
- **Information the agent can't see** can't be graded (Case 4). Check every fact in the rubric against the prompt and environment.
- **Fair failures should be left alone** (Case 1). Not every failed task needs a fix, and restraint matters.
- **Dependent values** such as totals should be checked against the agent's own cart.

## Note template I use

> **Call:** KEEP / FIX / FLAG
> **Evidence:** the specific listing, step number or calculation that decides it
> **Change:** the exact criterion rewritten, or why it can't be saved
