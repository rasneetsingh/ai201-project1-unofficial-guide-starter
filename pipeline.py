"""
Milestone 3 — Document ingestion + chunking for the F-1 Unofficial Guide.

Pipeline stages implemented here (see planning.md → Architecture):
    Document Ingestion  -> load_documents()   read every .txt in documents/
    Cleaning            -> clean_text()       normalize whitespace / strip boilerplate
    Chunking            -> chunk_text()       paragraph + bullet aware, ~500 chars, ~75 overlap

Chunking strategy (planning.md → Chunking Strategy):
  - Chunk size ~500 chars, overlap ~75 chars (~15%).
  - Documents are STRUCTURALLY HETEROGENEOUS, so a fixed character split is wrong:
      * very short single-fact docs (banking) must survive as ONE chunk,
      * long structured guides (visapp: STEP 1/2/3 + bulleted Q&A) must split on
        content boundaries (blank lines, bullets) so a point is never severed from
        its heading mid-sentence.
  - Overlap keeps adjacent sub-points connected for multi-part answers.

Run directly to load, clean, chunk, and inspect:
    python pipeline.py
"""

import glob
import html
import os
import re
import unicodedata

DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")

# Original source URL for each document, used for citation/attribution instead of
# the raw filename. (See README → Document Sources.) banking has no public URL.
SOURCE_URLS = {
    "f1_student_day1cpt.txt": "https://www.reddit.com/r/Day1CPTuniversities/comments/1ny23ip/guide_day_1_cpt_application_step_by_step/",
    "f1_student_opt.txt": "https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students",
    "f1_student_h1b.txt": "https://oia.osu.edu/international-scholars/h-1b-workers/h-1b-step-step-process",
    "f1_student_investing.txt": "https://www.reddit.com/r/f1visa/comments/1gyc6sk/can_f1_students_in_the_us_make_investments/",
    "f1_students_jobsearch.txt": "https://www.reddit.com/r/PhD/comments/1jcr56m/struggling_with_job_hunting_as_an_f1_student_need/",
    "f1_student_health.txt": "https://www.reddit.com/r/f1visa/comments/1pkmcfs/these_are_the_worst_insurance_a_student_can_get/",
    "f1_student_employment.txt": "https://www.reddit.com/r/f1visa/comments/1fbakb7/are_students_on_an_f1_visa_allowed_to_work_during/",
    "f1_student_visapp.txt": "https://www.reddit.com/r/IntltoUSA/comments/1sth1tg/three_steps_to_prepare_for_your_f1_us_student/",
    "f1_student_tax.txt": "https://www.reddit.com/r/tax/comments/1rofo6m/taxes_for_international_students/",
    "f1_student_banking.txt": "",  # no public URL collected for this source
}


def source_url(filename):
    """Return the citation URL for a document, falling back to the filename."""
    return SOURCE_URLS.get(filename) or filename

# Final chunking parameters (within the 400–600 char / 10–15% overlap range in planning.md).
CHUNK_SIZE = 500     # target max characters per chunk
OVERLAP = 75         # characters of context carried from one chunk into the next (~15%)


# --------------------------------------------------------------------------- #
# Stage 1: Document ingestion
# --------------------------------------------------------------------------- #
def load_documents(documents_dir=DOCUMENTS_DIR):
    """Read every .txt file in documents_dir.

    Returns a list of dicts: {"source": <filename>, "raw": <raw text>}.
    Sorted by filename so output is deterministic across runs.
    """
    docs = []
    for path in sorted(glob.glob(os.path.join(documents_dir, "*.txt"))):
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if raw.strip():  # skip empty files (e.g. a stray .gitkeep would be .txt-less anyway)
            docs.append({"source": os.path.basename(path), "raw": raw})
    return docs


# --------------------------------------------------------------------------- #
# Stage 2: Cleaning
# --------------------------------------------------------------------------- #
def clean_text(text):
    """Normalize a raw document into clean substantive text.

    Our sources are hand-copied plain text (no HTML/nav), so cleaning here is
    mostly whitespace and unicode normalization, with defensive HTML handling
    in case any source is pasted from a page later.
    """
    # Defensive: decode HTML entities (&amp;, &#39;, &nbsp;) and strip any stray tags.
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize unicode: smart quotes/dashes -> ascii so jargon (1040NR, 5–6) is consistent.
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    text = unicodedata.normalize("NFKC", text)

    # Normalize line endings and strip trailing spaces from every line.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]

    # Collapse runs of blank lines (our docs use " " spacer lines) into a single blank line.
    cleaned_lines = []
    blank = False
    for ln in lines:
        if ln.strip() == "":
            if not blank:
                cleaned_lines.append("")
            blank = True
        else:
            cleaned_lines.append(ln)
            blank = False

    return "\n".join(cleaned_lines).strip()


# --------------------------------------------------------------------------- #
# Stage 3: Chunking
# --------------------------------------------------------------------------- #
def _split_into_segments(text):
    """Split cleaned text into the smallest natural units we never want to break:
    paragraphs (blank-line separated) and bullet lines (lines starting with - or •).
    """
    # Break on a blank line, OR on a newline immediately preceding a bullet marker.
    parts = re.split(r"\n\s*\n|\n(?=\s*[-•])", text)
    return [p.strip() for p in parts if p.strip()]


# Abbreviations whose internal "." must NOT be treated as a sentence end.
_ABBREVIATIONS = ["e.g.", "i.e.", "vs.", "etc.", "approx.", "U.S.", "U.K.",
                  "Inc.", "Ltd.", "Dr.", "Mr.", "Ms.", "Mrs.", "Jr.", "Sr.", "St."]
_DOT = "\x00"  # placeholder swapped in for abbreviation dots during splitting


def _split_sentences(segment):
    """Fallback splitter for a single segment longer than CHUNK_SIZE.
    Splits after sentence-ending punctuation followed by whitespace, but protects
    common abbreviations (e.g. "vs.", "e.g.", "U.S.") so they aren't mis-split.
    """
    protected = segment
    for abbr in _ABBREVIATIONS:
        protected = protected.replace(abbr, abbr.replace(".", _DOT))
    sentences = re.split(r"(?<=[.!?])\s+", protected)
    return [s.replace(_DOT, ".").strip() for s in sentences if s.strip()]


def _tail_overlap(chunk, overlap):
    """Return trailing context (~overlap chars) of chunk to prepend to the next chunk.

    Snaps to a SENTENCE boundary so the next chunk begins at a sentence start rather
    than mid-sentence — this keeps each chunk self-contained while still carrying the
    connecting context that overlap is meant to provide.
    """
    if overlap <= 0 or len(chunk) <= overlap:
        return ""
    sentences = _split_sentences(chunk)
    if not sentences:
        return ""
    last = sentences[-1].strip()
    # Carry the last full sentence as continuity context, but only when it is a
    # reasonable standalone size. If the trailing sentence is very long, carry
    # nothing rather than a mid-sentence fragment — a clean sentence start beats
    # partial overlap. (Packing also drops the carry if it wouldn't leave room.)
    return last if len(last) <= max(overlap * 2, 200) else ""


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split one cleaned document into self-contained chunks.

    Strategy:
      1. If the whole doc fits in chunk_size, return it as ONE chunk (short docs).
      2. Otherwise split into natural segments (paragraphs / bullets) and greedily
         pack them up to chunk_size, never breaking a segment unless it alone
         exceeds chunk_size (then fall back to sentence splitting).
      3. Carry ~overlap chars of the previous chunk into the next for continuity.
    """
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    # Build the list of atomic segments, breaking over-long ones into sentences.
    segments = []
    for seg in _split_into_segments(text):
        if len(seg) <= chunk_size:
            segments.append(seg)
        else:
            for sentence in _split_sentences(seg):
                if len(sentence) <= chunk_size:
                    segments.append(sentence)
                else:
                    # Pathological long sentence: hard-wrap on word boundaries.
                    words, buf = sentence.split(), ""
                    for w in words:
                        if buf and len(buf) + 1 + len(w) > chunk_size:
                            segments.append(buf)
                            buf = w
                        else:
                            buf = f"{buf} {w}".strip()
                    if buf:
                        segments.append(buf)

    # Greedily pack segments into chunks, with character overlap between them.
    chunks = []
    current = ""
    for seg in segments:
        if not current:
            current = seg
        elif len(current) + 1 + len(seg) <= chunk_size:
            current = f"{current}\n{seg}"
        else:
            chunks.append(current)
            carry = _tail_overlap(current, overlap)
            # Start the next chunk with overlap context, then this segment.
            if carry and len(carry) + 1 + len(seg) <= chunk_size:
                current = f"{carry}\n{seg}"
            else:
                current = seg
    if current:
        chunks.append(current)

    # Safety net: never emit empty/whitespace-only chunks.
    return [c.strip() for c in chunks if c.strip()]


def build_corpus(documents_dir=DOCUMENTS_DIR, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Full pipeline: load -> clean -> chunk every document.

    Returns a list of chunk dicts with metadata:
        {"id", "source", "chunk_index", "text", "n_chars"}
    The source filename is attached to every chunk so retrieval can cite it.
    """
    corpus = []
    for doc in load_documents(documents_dir):
        cleaned = clean_text(doc["raw"])
        for i, chunk in enumerate(chunk_text(cleaned, chunk_size, overlap)):
            corpus.append({
                "id": f"{doc['source']}::chunk_{i}",
                "source": doc["source"],
                "source_url": source_url(doc["source"]),
                "chunk_index": i,
                "text": chunk,
                "n_chars": len(chunk),
            })
    return corpus


# --------------------------------------------------------------------------- #
# Inspection / verification (Milestone 3 checkpoint)
# --------------------------------------------------------------------------- #
def _print_inspection(corpus):
    n = len(corpus)
    sizes = [c["n_chars"] for c in corpus]
    print(f"\nLoaded {len(set(c['source'] for c in corpus))} documents.")
    print(f"Total chunks: {n}")
    print(f"Chunk size chars  -> min {min(sizes)}, max {max(sizes)}, "
          f"avg {sum(sizes) // n}")

    # Per-document chunk counts (verifies metadata + that short docs stay whole).
    print("\nChunks per document:")
    per_doc = {}
    for c in corpus:
        per_doc.setdefault(c["source"], 0)
        per_doc[c["source"]] += 1
    for src, count in sorted(per_doc.items()):
        print(f"  {src:32s} {count:3d} chunk(s)")

    # Health checks the checkpoint asks for.
    empties = [c for c in corpus if not c["text"].strip()]
    html_left = [c for c in corpus if re.search(r"<[^>]+>|&[a-z]+;|&#\d+;", c["text"])]
    print(f"\nHealth check -> empty chunks: {len(empties)}, "
          f"HTML/entity artifacts: {len(html_left)}")
    if 50 <= n <= 2000:
        print(f"Chunk count {n} is in the healthy 50–2000 range.")
    else:
        print(f"WARNING: chunk count {n} is outside the 50–2000 guidance range.")

    # 5 representative chunks: shortest, longest, and 3 spread across the corpus.
    print("\n" + "=" * 72)
    print("5 SAMPLE CHUNKS (read each: is it self-contained?)")
    print("=" * 72)
    by_size = sorted(corpus, key=lambda c: c["n_chars"])
    picks = [by_size[0], by_size[-1], corpus[n // 4], corpus[n // 2], corpus[3 * n // 4]]
    seen = set()
    for c in picks:
        if c["id"] in seen:
            continue
        seen.add(c["id"])
        print(f"\n--- [{c['source']}  chunk_{c['chunk_index']}  {c['n_chars']} chars] ---")
        print(c["text"])


if __name__ == "__main__":
    corpus = build_corpus()
    _print_inspection(corpus)
