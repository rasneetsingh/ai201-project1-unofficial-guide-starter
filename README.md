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
| 10 | Opening a bank account | Reddit Q&A (r/f1visa) | `documents/f1_student_banking.txt` | https://www.reddit.com/r/f1visa/comments/1pmim77/f1_student_need_advice_on_starting_a_bank_account/ |

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

Grounding is enforced **two ways** (see `query.py`), so the system can't fall back on the LLM's
training knowledge:

**1. Structural gate (before the LLM is ever called).** Retrieval returns chunks with a cosine
distance. If the *closest* chunk is farther than `IN_SCOPE_THRESHOLD = 0.55`, the question is
treated as out-of-scope and the system returns the fixed refusal **without calling the LLM at all**
— so for off-topic questions there is no opportunity to hallucinate. Chunks farther than
`CONTEXT_THRESHOLD = 0.62` are also dropped from the context so loosely-related text can't dilute
the answer. The model is also called with `temperature=0` for deterministic, grounded output.

**System prompt grounding instruction** (the actual instruction, not a paraphrase):

> You are a careful assistant that answers questions for international students on F-1 visas, using
> ONLY the context documents provided by the user.
> Rules:
> - Answer using only facts stated in the context documents below. Do NOT use any outside or prior
>   knowledge.
> - If the context does not contain enough information to answer the question, reply with EXACTLY
>   this sentence and nothing else: "I don't have enough information on that."
> - Do not guess, do not infer beyond what the text says, and do not add general advice that is not
>   in the context.
> - These are community/forum sources, so attribute claims to the source URL shown with each context
>   document, e.g. (source: https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/).
>   Use the exact URL from the context; never invent or shorten links, and cite each distinct URL at
>   most once.

Each document's **original source URL** (the Reddit thread, USCIS page, etc. from the Document
Sources table) is stored as chunk metadata in `pipeline.py` (`SOURCE_URLS`) and carried through the
vector store. The retrieved chunks are passed in the user message as a numbered, URL-labeled context
block (`[1] (source: https://www.reddit.com/r/...) <chunk text>`), so the model cites the real link
rather than a filename.

**How source attribution is surfaced in the response:** Two layers. (a) **Programmatically
guaranteed** — `ask()` returns a `sources` list of the **source URLs** built from the *metadata of
the chunks actually passed to the model*, not from anything the LLM writes; the Gradio UI shows these
in a dedicated "Retrieved from" box. (b) **Inline** — the model cites `(source: <url>)` next to
claims; a small post-processing step (`_dedupe_citations`) collapses any repeated URL within a
citation so links aren't listed multiple times. If the model returns the refusal, the `sources` list
is cleared so we never attribute a non-answer. *(If a document ever lacks a source URL, the citation
falls back to its filename.)*

### Example Responses

**Example 1 — grounded, source attributed** (input: *"Do I need an SSN or ITIN to open a US bank
account as an F-1 student?"*):
> You don't need an SSN or ITIN to open a bank account as an F-1 student. You can open a bank
> account with your passport, US address proof, US phone number, and the SSN equivalent of your home
> country **(source: https://www.reddit.com/r/f1visa/comments/1pmim77/f1_student_need_advice_on_starting_a_bank_account/)**.

*Retrieved from:* https://www.reddit.com/r/f1visa/comments/1pmim77/f1_student_need_advice_on_starting_a_bank_account/, https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/

**Example 2 — grounded, source attributed** (input: *"Why can't F-1 students use TurboTax, and what
should they use instead?"*):
> F-1 students can't use TurboTax because TurboTax does not support Form 8843 and Form 1040NR, which
> are required for nonresident aliens **(source: https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/)**.
> Instead, they can use alternatives such as Sprintax, F1TaxReturn, OLT, Glacier Tax Prep, or fill
> out the forms themselves **(source: https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/)**.

*Retrieved from:* https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/, https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/

**Example 3 — out-of-scope refusal** (input: *"What is the best pizza topping in New York City?"*):
> I don't have enough information on that.

*Retrieved from:* (no sources — the structural gate caught it; the LLM was never called.)

### Query Interface

A Gradio web UI (`app.py`, run with `python app.py` → http://localhost:7860):
- **Input** — a single "Your question" textbox (submit with the **Ask** button or Enter). Four
  clickable example questions are provided so a viewer can use it without instruction.
- **Output** — an **Answer** box (the grounded response, with inline source links) and a
  **Retrieved from** box listing the source URL(s) the answer was drawn from.

**Sample interaction transcript:**
```
Your question:  Can F-1 students legally invest in stocks, and how are gains taxed?

Answer:         Yes, F-1 students can legally invest in stocks (source:
                https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/).
                The main thing to avoid is day trading. F-1 students may be taxed a
                flat 30% on investment gains, regardless of long-term vs. short-term
                capital gains or tax bracket (source: .../1gyc6sk/...).

Retrieved from: • https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/
                • https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

All 5 questions were run through the full pipeline (`ask()` in `query.py`, top-k=5). Source of
each top hit and its cosine distance are shown for transparency.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Do I need an SSN/ITIN to open a US bank account? | No — passport, US address proof, US phone number, and home-country ID number are enough. | "No… passport, US address proof, US phone number, and the SSN equivalent of your home country" — cites `banking.txt`. Top hit `banking.txt` @ 0.329. | Relevant | **Accurate** |
| 2 | Work hours on campus: summer vs. in session? | 40 hrs/week when school is out; max 20 hrs/week when classes in session. | "Up to 40 hours per week on campus during summer… cannot work more than 20 hours/week when classes are in session" — cites `employment.txt`. Top hit `employment.txt` @ 0.337. | Relevant | **Accurate** |
| 3 | Can F-1 students invest, and how are gains taxed? | Yes (avoid day trading); gains may be a flat 30% as a nonresident. | "Yes… avoid day trading… may be taxed a flat 30% on investment gains regardless of long-term vs. short-term" — cites `investing.txt`. Top hit `investing.txt` @ 0.321. | Relevant | **Accurate** |
| 4 | Why can't F-1 students use TurboTax, what instead? | File 8843/1040NR as nonresident aliens (TurboTax can't); use Sprintax, Glacier, OLT, F1TaxReturn, or VITA. | "TurboTax does not support Form 1040NR… use Sprintax, F1TaxReturn, or OLT" — cites `tax.txt`. Top hit `tax.txt` @ 0.308. | Relevant | **Accurate** (minor omission — names 1040NR but not Form 8843; lists 3 of 5 tools) |
| 5 | Does pre-completion OPT reduce post-completion OPT? | Yes — 1 yr full-time pre-completion removes all post-completion OPT; 1 yr part-time removes 6 months. | "Yes… 1 year part-time pre-completion OPT reduces full-time OPT by 6 months; 1 year full-time reduces it by 1 year" — cites `opt.txt`. Top hit `opt.txt` @ 0.399. | Relevant | **Accurate** |

**Summary:** 5/5 questions returned the correct source document as the #1 hit with top distances
0.308–0.399 (all well under 0.5), and 5/5 answers were accurate. Q4 is accurate but slightly
incomplete — it omits Form 8843 and two of the five filing tools, because the chunk naming 8843
(`tax.txt` c0, the OP's question block) ranked #2 while the answer drew mainly from the higher-ranked
`tax.txt` c1. This is a completeness gap, not an error.

**Legend — Retrieval quality:** Relevant / Partially relevant / Off-target  
**Legend — Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** *"Can I take a summer consulting internship under OPT, and is sponsorship
hard?"* (This is the cross-document failure candidate flagged in planning.md → Anticipated
Challenges #2.)

**What the system returned:** *"…it is possible to take a consulting job on OPT (source:
f1_students_jobsearch.txt). However, the job must be directly related to your major area of study
(source: f1_student_opt.txt). Regarding sponsorship, the US job market is rough… very difficult…"*
The answer affirms doing a **summer** internship **on OPT** and never delivers the single most
important caveat: you should **not** use OPT in the summer — summer off-campus work should be done
under **CPT**, because pre-completion OPT used in summer eats into your post-completion OPT.

**Root cause (tied to a specific pipeline stage): the retrieval stage (top-k cutoff), not
generation.** The decisive fact lives in `f1_student_employment.txt` chunk c3: *"Important warning
on OPT vs. CPT during summer: Do NOT use OPT during the summer… Summer off-campus work should be
done under CPT."* When I retrieved with k=15, that chunk ranked **#10 at cosine distance 0.629** —
far outside the top-5 the generator actually sees. The query's wording ("consulting internship",
"OPT", "sponsorship") is semantically closest to `jobsearch.txt` (whose OP literally asks "is it
possible to take a consulting job on OPT?") and to the OPT-definition chunks, so cosine similarity
filled all 5 slots with those, crowding out the employment-doc caveat. This is the classic
cross-document problem: a complete answer must **synthesize two documents** — `employment.txt` (use
CPT not OPT in summer) and `jobsearch.txt` (consulting + sponsorship is hard) — but top-k=5 with
pure semantic similarity pulled almost entirely from one side. Generation then did its job correctly
*given the chunks it had*; it was faithful to a context that was missing the key fact. The grounding
worked (no hallucination) — retrieval recall was the failure.

**What you would change to fix it:** Options, roughly in order of effort: (1) **raise k** (e.g.,
k=8–10) so chunk c3 at rank #10 makes the window — cheap, but adds noise to every query; (2)
**MMR / diversity re-ranking** so the context isn't dominated by near-duplicate chunks from one
document, forcing inclusion of other relevant sources; (3) **hybrid retrieval** (semantic + keyword
BM25) so the literal terms "summer" and "CPT" in c3 get weighted up; (4) **query expansion** — embed
the question alongside a rephrase ("summer internship work authorization CPT vs OPT") to pull in the
timing-focused chunk. I'd try MMR re-ranking first, since the root cause is one document
monopolizing the top-k rather than the right chunk being un-embeddable.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The Chunking Strategy section forced me to
confront *document heterogeneity* before writing any code — I had already reasoned that `banking`
(one sentence) must stay a single chunk while `visapp` (a long STEP 1/2/3 guide with a bulleted Q&A)
must split on content boundaries. That ruled out the naive fixed-character splitter and pointed me
straight at a paragraph- and bullet-aware chunker. The payoff showed up two milestones later: clean,
self-contained chunks meant retrieval "just worked" on the first try (top distances 0.31–0.40, 5/5
correct sources) with no debugging loop. The spec also paid off in the failure analysis — Anticipated
Challenge #2 predicted the exact cross-document question that broke retrieval, so I knew where to
look.

**One way your implementation diverged from the spec, and why:** My AI Tool Plan described grounding
as a *prompt-only* mechanism (Milestone 5: "instruct the model to answer only from context… refusing
when context is insufficient"). In implementation I added a second, **structural** layer the spec
didn't anticipate: a cosine-distance relevance gate in `query.py` that refuses out-of-scope questions
**before the LLM is ever called** (and drops low-relevance chunks from the context). I diverged
because prompt-only grounding still hands the model loosely-related chunks for an off-topic query,
leaving room for a confident-but-unfounded answer; gating on retrieval distance closes that hole
deterministically. A second, smaller divergence: the instructions specified `gradio>=6.9.0`, but that
requires Python 3.10+ and my environment is Python 3.9.6, so I pinned to gradio 4.44.1 (identical
`gr.Blocks` API).

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — Implementing the chunker**

- *What I gave the AI:* My planning.md Chunking Strategy section and the actual documents, with the
  instruction to implement `load_documents()` and `chunk_text()` matching my spec (500 chars,
  ~75-char overlap, short docs stay whole, long guides split on content boundaries).
- *What it produced:* A paragraph- and bullet-aware packer. On the first run it worked, but when I
  inspected the output (the chunk-inspection step), several chunks started mid-sentence because the
  overlap snapped to a *word* boundary, and one investing chunk broke at "vs."
- *What I changed or overrode:* I directed two fixes rather than accepting the first output: (1)
  change the overlap to carry a whole *trailing sentence* so no chunk begins mid-sentence, and (2)
  protect abbreviations (`vs.`, `e.g.`, `U.S.`) from the sentence splitter. I re-verified and
  confirmed 0/79 chunks start mid-sentence. The inspection-and-iterate loop was the point — I didn't
  take the generated code as final.

**Instance 2 — Grounding the generation step**

- *What I gave the AI:* My grounding requirement (answer from retrieved context only, refuse when
  insufficient, attribute sources) and asked it to wire up generation with Groq.
- *What it produced:* A working `ask()` with a strict system prompt — i.e., *prompt-only* grounding,
  which is what my planning.md AI Tool Plan had described.
- *What I changed or overrode:* I wasn't satisfied that a prompt alone would stop the model from
  answering off-topic questions from training knowledge, so I directed adding a *structural* layer:
  a cosine-distance relevance gate that refuses before the LLM is called, plus building the `sources`
  list programmatically from chunk metadata instead of trusting the LLM to cite. I tested with an
  out-of-scope question ("best pizza topping in NYC") to confirm the gate fires and the system
  refuses.
