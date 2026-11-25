# 🧪 Lab notes

I run a small AI lab at home: one Windows PC with one 16 GB graphics card (RTX 4070 Ti SUPER). I pick the questions, set the rules and make the calls. AI coding agents (Claude, and Codex until November 2026) write most of the code under those rules: one builds, another checks the work on its own. These notes are what I measured, including what failed.

**My rules**

- I write the pass bar down before the run. A tiny script for that is in [`lab/prereg_log.py`](lab/prereg_log.py).
- Every arm of a test gets the same settings.
- Failures stay in the notes.
- Test text is made up or public. No private chats, ever.
- A number comes with three things: what it counts, how many, and which way is better.

## 1. A language model trained from zero

I trained a 62.6-million-parameter model on this PC, from random numbers up: 27,000 steps, three passes over 295.3 million tokens of an Apache-2.0 text set. Before training I removed the 0.11% of documents that overlapped the test questions, so known copies of the tests were out of the training text.

| Test (higher is better) | My model | Guessing | A public 360M model |
| --- | --- | --- | --- |
| HellaSwag | 29.4% | 25% | 57.2% |
| ARC-Easy | 38.3% | 25% | 55.4% |
| ARC-Challenge | 24.8% | 25% | not listed |
| WinoGrande | 51.9% | 50% | not listed |

**What it taught me:** it is above guessing on two of these and at guessing on the other two. It is a learning project, not an assistant. The weights are not published.

## 2. Faster replies from one engine setting

One setting makes the engine read a long prompt in bigger batches. In two lab tests it cut a reply's time by 17% and 28% (lower time is better). The speed came from two causes, and I first had that half wrong. The correction is in my log.

## 3. Thinking only when unsure

On 224 questions whose answer was **not** in the notes, I counted how often a 4-billion-parameter model made one up (lower is better). The bar was set before this run, on questions I had not looked at. The middle column is put together from the other two runs, not a run of its own.

| | Fast mode | Thinks only when unsure | Always thinks |
| --- | --- | --- | --- |
| Made-up answers | 42.0% | 19.6% | 12.1% |
| Seconds per reply, average | 0.12 | 4.87 | 10.27 |

**What I want to try next:** teach the fast mode to be as honest as the thinking mode, by training the model on its own thinking.

## 4. Old news told as new

I asked local models about 25 public events from September to November 2026, without naming the year ("who won the most recent ...?"). Today's date was in the prompt. On a plain prompt one 35B model gave an old or wrong winner as the current one in 18 of 25 answers (lower is better). Inside my assistant's own prompt the same model did it in 3 of 25 and said it could not check in 18 of 25. I labelled those by hand. It is a pilot test: I have not yet proved which line of the prompt does it.

## 5. Things that did not work

- **A smarter way to shrink a 35B model.** It said "unknown" when the answer was right there in 20.5% of cases, against 9.4% before (lower is better). Not used.
- **A faster prompt layout.** The first version looked 30 to 45% faster. It also changed how the assistant talks. I tried five versions. None passed every bar, so none shipped.
- **New rules for a text filter.** On the list they were tuned on, false alarms fell from 194 to 85. On a sealed list nobody had tuned on, they went from 6 to 6. They only fit their own examples, so they did not ship. This is my favorite result, because the test caught it before I believed it.

## What I am not claiming

I am a beginner with a cybersecurity focus. These are small tests on one PC, and most have not been repeated by anyone else. If something here is wrong, I want to know.
