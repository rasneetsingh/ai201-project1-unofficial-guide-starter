"""
Milestone 5 — Grounded generation for the F-1 Unofficial Guide.

Pipeline stage (see planning.md → Architecture):
    Generation -> ask()   retrieve top-k chunks, ground an LLM answer in them only,
                          and attach source attribution programmatically.

Grounding is enforced two ways (belt and suspenders):
  1. STRUCTURAL: a relevance gate. If the closest chunk's cosine distance is above
     IN_SCOPE_THRESHOLD, the question is treated as out-of-scope and we refuse WITHOUT
     calling the LLM — so it can never answer from training knowledge.
  2. PROMPT: a system prompt that instructs the model to use ONLY the provided context
     and to reply with a fixed refusal string when the context is insufficient.

Source attribution is GUARANTEED programmatically: result["sources"] is built from the
metadata of the chunks actually passed to the model, not from whatever the LLM writes.

    from query import ask
    ask("Do I need an SSN to open a bank account?")
"""

import os

from dotenv import load_dotenv
from groq import Groq

from retrieval import retrieve

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

LLM_MODEL = "llama-3.3-70b-versatile"
TOP_K = 5
# Cosine distance gates (calibrated against Milestone 4: real answers scored 0.31–0.40,
# loosely-related noise 0.5–0.6, off-topic queries > 0.6).
IN_SCOPE_THRESHOLD = 0.55   # if the best chunk is farther than this, refuse up front
CONTEXT_THRESHOLD = 0.62    # chunks farther than this are dropped from the context

REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = """You are a careful assistant that answers questions for international \
students on F-1 visas, using ONLY the context documents provided by the user.

Rules:
- Answer using only facts stated in the context documents below. Do NOT use any outside \
or prior knowledge.
- If the context does not contain enough information to answer the question, reply with \
EXACTLY this sentence and nothing else: "{refusal}"
- Do not guess, do not infer beyond what the text says, and do not add general advice \
that is not in the context.
- These are community/forum sources, so when relevant, attribute claims to the source \
filename, e.g. (source: f1_student_tax.txt).""".format(refusal=REFUSAL)

_client = None


def get_client():
    """Construct (and cache) the Groq client from GROQ_API_KEY in .env."""
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key or key == "your_key_here":
            raise RuntimeError("GROQ_API_KEY is missing — set it in .env")
        _client = Groq(api_key=key)
    return _client


def _format_context(chunks):
    """Render retrieved chunks into a numbered, source-labeled context block."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        blocks.append(f"[{i}] (source: {c['source']})\n{c['text']}")
    return "\n\n".join(blocks)


def ask(question, k=TOP_K):
    """Answer a question grounded in retrieved chunks.

    Returns {"answer", "sources", "chunks", "grounded"} where:
      - answer: the LLM answer, or the fixed refusal for out-of-scope questions
      - sources: unique source filenames of the chunks used (guaranteed, may be empty)
      - chunks: the retrieved chunks passed as context (with distances)
      - grounded: False when we refused up front (no LLM call), True otherwise
    """
    hits = retrieve(question, k=k)

    # Structural grounding gate: nothing close enough -> refuse without calling the LLM.
    if not hits or hits[0]["distance"] > IN_SCOPE_THRESHOLD:
        return {"answer": REFUSAL, "sources": [], "chunks": [], "grounded": False}

    # Keep only chunks relevant enough to be useful context.
    context_chunks = [h for h in hits if h["distance"] <= CONTEXT_THRESHOLD]
    sources = sorted({c["source"] for c in context_chunks})

    user_message = (
        f"Context documents:\n\n{_format_context(context_chunks)}\n\n"
        f"Question: {question}"
    )

    completion = get_client().chat.completions.create(
        model=LLM_MODEL,
        temperature=0,  # deterministic, grounded — no creative drift
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    answer = completion.choices[0].message.content.strip()

    # If the model refused, don't attach sources (it didn't actually use them).
    if answer == REFUSAL:
        sources = []
    return {"answer": answer, "sources": sources, "chunks": context_chunks, "grounded": True}


if __name__ == "__main__":
    tests = [
        "Do I need an SSN or ITIN to open a US bank account as an F-1 student?",
        "Why can't F-1 students use TurboTax, and what should they use instead?",
        "Does using pre-completion OPT reduce my post-completion OPT time?",
        "What is the best pizza topping in New York City?",  # out-of-scope
    ]
    for q in tests:
        r = ask(q)
        print("=" * 78)
        print("Q:", q)
        print("A:", r["answer"])
        print("Sources:", ", ".join(r["sources"]) if r["sources"] else "(none)")
        if r["chunks"]:
            print("Top distance:", round(r["chunks"][0]["distance"], 3))
