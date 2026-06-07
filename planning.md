# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

**The F-1 international student experience in the US.** A retrieval system over the practical,
day-to-day knowledge an F-1 visa holder needs: work authorization (CPT/OPT), the H-1B and
visa-interview process, taxes, banking, health insurance, investing, and the job search.

Official sources (USCIS, university international offices) cover the *legal rules* but rarely the
*lived experience* — which documents a bank will actually accept without an SSN, whether the cheap
"student" insurance plans actually pay out, which tax software works for nonresidents, or what a
visa officer is really probing for. That practical knowledge is scattered across Reddit threads,
YouTube transcripts, and word-of-mouth, and getting it wrong has high-stakes consequences for visa
status. This system makes that scattered knowledge searchable in one place.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit — r/Day1CPTuniversities | Step-by-step Day 1 CPT application guide | https://www.reddit.com/r/Day1CPTuniversities/comments/1ny23ip/guide_day_1_cpt_application_step_by_step/ |
| 2 | USCIS (official) | Pre- and post-completion OPT rules | https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students |
| 3 | Ohio State OIA | H-1B sponsorship step-by-step process & timelines | https://oia.osu.edu/international-scholars/h-1b-workers/h-1b-step-step-process |
| 4 | Reddit — r/f1visa | Can F-1 students invest? Brokerages, day trading, 30% tax | https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/ |
| 5 | Reddit — r/PhD | Job hunting on F-1, sponsorship, OPT unemployment workaround | https://www.reddit.com/r/PhD/comments/1jcr56m/struggling_with_job_hunting_as_an_f1_student_need/ |
| 6 | Reddit — r/f1visa | Health insurance — why cheap plans fail, ACA, university plans | https://www.reddit.com/r/f1visa/comments/1pkmcfs/these_are_the_worst_insurance_a_student_can_get/ |
| 7 | Reddit — r/f1visa | Part-time / summer work hour limits (20 vs 40) and CPT vs OPT | https://www.reddit.com/r/f1visa/comments/1fbakb7/are_students_on_an_f1_visa_allowed_to_work_during/ |
| 8 | Reddit — r/IntltoUSA | Three-step framework to prepare for the F-1 visa interview | https://www.reddit.com/r/IntltoUSA/comments/1sth1tg/three_steps_to_prepare_for_your_f1_us_student/ |
| 9 | Reddit — r/tax | Nonresident tax filing (8843/1040NR), Sprintax/Glacier/OLT/VITA | https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/ |
| 10 | Reddit — r/f1visa | Opening a US bank account without an SSN/ITIN | https://www.reddit.com/r/f1visa/comments/1pmim77/f1_student_need_advice_on_starting_a_bank_account/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** **500 characters** target max (~125 tokens) — *finalized in Milestone 3.*

**Overlap:** **~75 characters (~15%)**, carried as a whole trailing **sentence** (not a raw
character slice) so chunks never begin mid-sentence.

**Final result (Milestone 3):** 79 chunks across 10 documents (min 153 / max 499 / avg 387 chars);
`banking` stays 1 chunk, `visapp` splits into 19. Implemented in `pipeline.py` as a
**paragraph- and bullet-aware packer** rather than a fixed character split.

**Reasoning:** My documents are **structurally heterogeneous**, which is the central chunking
challenge:
- **Very short, single-fact docs** — `banking` (~51 words) is one paragraph where the whole answer
  is a single sentence. It should survive as **one chunk**; splitting it is pointless.
- **Long, structured guides** — `visapp` (~1,031 words) has labeled sections (STEP 1/2/3) plus a
  long bulleted Q&A. Facts are spread across many paragraphs, so one giant chunk dilutes retrieval,
  but splitting mid-section can sever a point from its heading.
- **Medium explainers** (~300–600 words) — `opt`, `tax`, `health`, `investing` — are a question
  followed by several distinct sub-points (e.g. the tax doc lists Sprintax / Glacier / OLT / VITA
  as separate options).

A single fixed size will over-split short docs and may fragment long ones. The small overlap keeps
adjacent sub-points connected for multi-part answers. Final size/overlap will be set empirically
after inspecting chunk boundaries on `visapp` and `tax`.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers (local, free, fast, 384-dim) —
*tentative.*

**Top-k:** 3–4 chunks per query.

**Production tradeoff reflection:** If cost weren't a constraint I'd weigh a larger hosted model
(e.g. OpenAI `text-embedding-3-large` or a Cohere multilingual model). Tradeoffs: (1) **context
length** — fine here since chunks are short; (2) **multilingual support** — relevant because some
F-1 questions mix in home-country terms, but my corpus is English; (3) **domain accuracy** — immigration
jargon (CPT, OPT, I-20, 1040NR, prevailing wage) is niche, so a stronger model may disambiguate
better; (4) **latency & local vs. API** — MiniLM runs locally with no API cost or rate limits, which
suits a student project; a hosted model adds latency and per-call cost for marginal accuracy gains.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

Each question maps to a specific document with a concrete, checkable answer.

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Do I need an SSN or ITIN to open a US bank account as an F-1 student? | No — passport, US address proof, US phone number, and your home-country ID number are enough. (`banking`) |
| 2 | How many hours can an F-1 student work on campus during summer vs. when classes are in session? | Up to 40 hrs/week when school is out of session; max 20 hrs/week total when classes are in session. (`employment`) |
| 3 | Can F-1 students legally invest in stocks, and how are gains taxed? | Yes (avoid day trading as a primary activity); gains may be taxed a flat 30% as a nonresident. (`investing`) |
| 4 | Why can't F-1 students use TurboTax, and what should they use instead? | They file Form 8843 / 1040NR as nonresident aliens, which TurboTax doesn't support; use Sprintax, Glacier, OLT, F1TaxReturn, or a VITA site. (`tax`) |
| 5 | Does using pre-completion OPT reduce my post-completion OPT time? | Yes — 1 yr full-time pre-completion OPT removes all post-completion OPT; 1 yr part-time removes 6 months. (`opt`) |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Key information split across chunk boundaries.** The `visapp` and long Q&A docs spread a single
   answer across many paragraphs. If a chunk cuts between a claim and its qualifier, retrieval may
   return only half the context and the model answers incompletely.

2. **Cross-document questions.** Some answers live in two docs at once — e.g. *"Can I take a summer
   consulting internship under OPT?"* is answered partly in `employment` (don't use OPT in summer;
   use CPT) and partly in `jobsearch` (consulting + sponsorship is hard). Top-k retrieval may pull
   chunks from only one document. **This is my planned failure-case candidate for Milestone 6.**

3. **Conflicting / inconsistent community advice.** Reddit threads contain disagreement (e.g. the
   `investing` doc has several conflicting takes on whether day trading is allowed). The model may
   surface one opinion as fact rather than reflecting the genuine disagreement.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
┌──────────────────┐   ┌──────────┐   ┌─────────────────────┐   ┌───────────┐   ┌────────────┐
│ Document         │   │ Chunking │   │ Embedding + Vector  │   │ Retrieval │   │ Generation │
│ Ingestion        │──▶│          │──▶│ Store               │──▶│           │──▶│            │
│ read 10 .txt     │   │ split +  │   │ all-MiniLM-L6-v2 →  │   │ embed     │   │ Groq LLM   │
│ files            │   │ overlap  │   │ vectors in store    │   │ query,    │   │ answers    │
│ (documents/)     │   │ (Py)     │   │ (ChromaDB)          │   │ top-k=3-4 │   │ from chunks│
└──────────────────┘   └──────────┘   └─────────────────────┘   └───────────┘   └────────────┘
```
*Stack: Python ingestion/chunking, `all-MiniLM-L6-v2` (sentence-transformers) embeddings,
ChromaDB vector store, Groq-hosted LLM for generation. Embedding model and top-k may be tuned
during implementation.*

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** Give Claude my *Chunking Strategy* section and ask it to
implement `load_documents()` (read every `.txt` in `documents/`) and `chunk_text()` with my chunk
size and overlap. Verify by printing the chunk count and eyeballing boundaries on `visapp` (long)
and `banking` (short) to confirm short docs stay as one chunk and sections aren't severed.

**Milestone 4 — Embedding and retrieval:** Give Claude my *Retrieval Approach* section and ask it to
embed chunks with `all-MiniLM-L6-v2`, build the vector store, and implement `retrieve(query, k)`.
Verify by running my 5 test questions and checking the top-k chunks come from the expected source
doc (e.g. Q4 → `tax`).

**Milestone 5 — Generation and interface:** Ask Claude to write the generation step + a simple CLI:
format retrieved chunks into a grounded prompt that instructs the model to answer only from context
and cite source filenames, refusing when context is insufficient. Verify with the cross-document
OPT/CPT question to see whether it grounds or hallucinates.
