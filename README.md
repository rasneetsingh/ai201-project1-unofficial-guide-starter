# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels? -->

This Unofficial Guide covers the practical, day-to-day realities of living in the US as an
international student on an **F-1 visa** — work authorization (CPT/OPT), the H-1B and visa-interview
process, taxes, banking, health insurance, investing, and the job search. Official sources like
USCIS and university international offices explain the *legal rules* but rarely the *lived
experience*: which documents a bank will actually accept without an SSN, whether the cheap
"student" insurance plans actually pay out, which tax software works for nonresidents, or what a
visa officer is really probing for. This knowledge is scattered across Reddit threads, YouTube
transcripts, and word-of-mouth — and getting it wrong carries high-stakes consequences for your
visa status.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Subtopic | Type | File | Original source URL |
|---|----------|------|------|---------------------|
| 1 | Day 1 CPT application steps | Reddit guide (r/Day1CPTuniversities) | `documents/f1_student_day1cpt.txt` | https://www.reddit.com/r/Day1CPTuniversities/comments/1ny23ip/guide_day_1_cpt_application_step_by_step/ |
| 2 | OPT (pre/post-completion) | Official — USCIS | `documents/f1_student_opt.txt` | https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students |
| 3 | H-1B sponsorship process | University office (Ohio State OIA) | `documents/f1_student_h1b.txt` | https://oia.osu.edu/international-scholars/h-1b-workers/h-1b-step-step-process |
| 4 | Investing as an F-1 student | Reddit Q&A (r/f1visa) | `documents/f1_student_investing.txt` | https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/ |
| 5 | Job search & OPT unemployment | Reddit Q&A (r/PhD) | `documents/f1_students_jobsearch.txt` | https://www.reddit.com/r/PhD/comments/1jcr56m/struggling_with_job_hunting_as_an_f1_student_need/ |
| 6 | Health insurance | Reddit Q&A (r/f1visa) | `documents/f1_student_health.txt` | https://www.reddit.com/r/f1visa/comments/1pkmcfs/these_are_the_worst_insurance_a_student_can_get/ |
| 7 | Part-time / summer work hours | Reddit Q&A (r/f1visa) | `documents/f1_student_employment.txt` | https://www.reddit.com/r/f1visa/comments/1fbakb7/are_students_on_an_f1_visa_allowed_to_work_during/ |
| 8 | Visa interview prep | Reddit guide (r/IntltoUSA) | `documents/f1_student_visapp.txt` | https://www.reddit.com/r/IntltoUSA/comments/1sth1tg/three_steps_to_prepare_for_your_f1_us_student/ |
| 9 | Taxes (nonresident filing) | Reddit Q&A (r/tax) | `documents/f1_student_tax.txt` | https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/ |
| 10 | Opening a bank account | Personal tip / forum note | `documents/f1_student_banking.txt` | _(no URL — add the source you collected this from)_ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters (target max, ≈125 tokens).

**Overlap:** ~75 characters (~15%), carried as a whole trailing **sentence** so no chunk begins
mid-sentence.

**Preprocessing before chunking** (`clean_text()` in `pipeline.py`): decode HTML entities and
strip any stray tags (defensive — sources are hand-copied plain text), normalize smart
quotes/dashes to ASCII so domain jargon (`1040NR`, `5-6 years`) is consistent, strip trailing
whitespace, and collapse the blank " " spacer lines the sources use into single blank lines.

**Why these choices fit your documents:** The corpus is **structurally heterogeneous**, so a fixed
character split is the wrong tool — it would over-split the one-sentence `banking` doc and sever
points from their headings in the long `visapp` guide. Instead, `chunk_text()` is **paragraph- and
bullet-aware**: it (1) keeps any document that fits in 500 chars as a single chunk (so `banking`
stays whole), (2) otherwise splits on natural boundaries — blank lines and bullet markers — and
greedily packs those segments up to 500 chars without breaking one, and (3) only falls back to
sentence splitting for a paragraph that is itself longer than 500 chars (with abbreviations like
`vs.`, `e.g.`, `U.S.` protected so sentences aren't mis-split). The ~75-char sentence overlap keeps
adjacent sub-points connected for multi-part answers.

**Final chunk count:** **79 chunks** across 10 documents (min 153 / max 499 / avg 387 chars;
0 empty, 0 HTML artifacts). Per-document counts scale with length: `banking` 1, `visapp` 19.

### Sample chunks (5 labeled, with source document)

**1. `f1_student_banking.txt` — chunk_0 (310 chars):**
> You don't need ITIN/SSN to open a bank account. Schedule an appointment at any bank and go. Take your passport, US address proof (lease agreement/electricity/wifi bill), US phone number, SSN equivalent of your home country (just the number is good enough. You don't need the actual card). That's pretty much it

**2. `f1_student_tax.txt` — chunk_1 (440 chars):**
> COMMENTS / ADVICE:
> Tax status basics: International students on F-1 visas are considered nonresident aliens for tax purposes for their first 5 years in the country. If you entered the US last year, you'll generally need to file Form 8843 and Form 1040NR - which TurboTax does not support. That's why F-1 students can't use TurboTax.
> Filing options people recommended:
> - Sprintax: similar to TurboTax but for nonresidents; expensive (~$105).

**3. `f1_student_opt.txt` — chunk_1 (446 chars):**
> If you are an F-1 student, you may be eligible to participate in OPT in two different ways:
> Pre-completion OPT: You may apply to participate in pre-completion OPT after you have been lawfully enrolled on a full-time basis for one full academic year at a college, university, conservatory, or seminary that has been certified by the U.S. Immigration and Customs Enforcement (ICE) Student and Exchange Visitor Program (SEVP) to enroll F-1 students.

**4. `f1_student_investing.txt` — chunk_1 (206 chars):**
> I'm on F1 and hold some stocks with Schwab.
> As long as you have an SSN, you can invest in stocks or open a high-yield savings account (HYSA).
> You can invest in stocks, cryptocurrency, ETFs, and real estate.

**5. `f1_student_visapp.txt` — chunk_1 (292 chars):**
> STEP 1 - HAVE A NARRATIVE:
> There is no single "good" answer for questions like "what will you do after graduation?" or "why this program?" What matters is that your narrative is (1) consistent with the law, (2) consistent with the rest of your narrative, and (3) consistent with common sense.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via sentence-transformers — a local, free, 384-dimensional
model. Chosen because it runs entirely on-device (no API key, no rate limits, no per-call cost),
is fast enough to embed all 79 chunks in under a second, and is accurate enough for a corpus this
small. Chunks and queries are embedded with `normalize_embeddings=True` and stored in ChromaDB
using **cosine** distance.

**Production tradeoff reflection:** If cost weren't a constraint I'd weigh a larger hosted model
(e.g. OpenAI `text-embedding-3-large` at 3,072 dims, or a Cohere multilingual model). Tradeoffs:
(1) **context length** — not a factor here since my chunks are short (≤500 chars); (2) **multilingual
support** — relevant because F-1 questions sometimes mix in home-country terms, though my corpus is
English; (3) **domain accuracy** — immigration jargon (CPT, OPT, I-20, 1040NR, prevailing wage) is
niche, so a stronger model might disambiguate better; (4) **latency & local vs. API** — MiniLM runs
locally with zero cost or rate limits, while a hosted model adds per-call latency and cost for
accuracy gains that are marginal at this scale. For 79 chunks, MiniLM is the right tradeoff.

### Retrieval Test Results

Vector store: **ChromaDB** (cosine distance, lower = more relevant), **top-k = 5**, embedded with
`all-MiniLM-L6-v2`. All 5 evaluation queries returned the correct source document as the #1 hit
with a top-result distance well under 0.5:

| Query | Top hit | Distance |
|-------|---------|----------|
| Do I need an SSN/ITIN to open a US bank account? | `f1_student_banking.txt` c0 | **0.329** |
| Work hours on campus: summer vs. in session? | `f1_student_employment.txt` c0 | **0.337** |
| Can F-1 students invest, and how are gains taxed? | `f1_student_investing.txt` c0 | **0.321** |
| Why can't F-1 students use TurboTax? | `f1_student_tax.txt` c1 | **0.308** |
| Does pre-completion OPT reduce post-completion OPT? | `f1_student_opt.txt` c4 | **0.399** |

**Why the returned chunks are relevant (2 explained):**

- *"Why can't F-1 students use TurboTax…"* → top chunk `f1_student_tax.txt` c1 (dist 0.308): this
  chunk directly states F-1 students are *"nonresident aliens… need to file Form 8843 and Form
  1040NR — which TurboTax does not support,"* then begins listing alternatives (Sprintax). The
  query never uses the words "nonresident" or "1040NR," yet semantic search matched it — that's the
  embedding capturing *meaning*, not keywords.
- *"Does pre-completion OPT reduce post-completion OPT?"* → top chunk `f1_student_opt.txt` c4 (dist
  0.399) is the section literally titled *"Impact of Pre-completion OPT… on Requests for
  Post-completion OPT,"* and the concrete answer (1 yr full-time removes all post-completion OPT;
  part-time removes 6 months) is in c5, also retrieved in the top-5. The relevant content is in the
  returned set.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
