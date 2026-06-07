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

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

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
