"""
Milestone 5 — Gradio query interface for the F-1 Unofficial Guide.

Run:
    python app.py
then open http://localhost:7860

Input:  a question about the F-1 student experience (work auth, taxes, banking, etc.)
Output: a grounded answer (answered only from the retrieved documents) plus the list
        of source documents the answer was retrieved from.
"""

import gradio as gr

from query import ask


def handle_query(question):
    """Run a question through the grounded RAG pipeline for the UI."""
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"]) or "(no sources — outside the guide)"
    return result["answer"], sources


EXAMPLES = [
    "Do I need an SSN or ITIN to open a US bank account as an F-1 student?",
    "Why can't F-1 students use TurboTax, and what should they use instead?",
    "Can F-1 students legally invest in stocks, and how are gains taxed?",
    "How many hours can an F-1 student work on campus during summer vs. in session?",
]

with gr.Blocks(title="The Unofficial F-1 Guide") as demo:
    gr.Markdown(
        "# The Unofficial F-1 Guide\n"
        "Ask about the practical F-1 international-student experience — work "
        "authorization (CPT/OPT), taxes, banking, health insurance, investing, "
        "visa interviews, and the job search. Answers come **only** from the "
        "collected community documents; if the guide doesn't cover it, the system "
        "will say so."
    )
    inp = gr.Textbox(label="Your question", placeholder="e.g. Do I need an SSN to open a bank account?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    gr.Examples(examples=EXAMPLES, inputs=inp)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
