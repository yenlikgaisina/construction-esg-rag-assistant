# 🏗 BuildLens AI

**Turn construction ESG documents into source-backed decisions.**

BuildLens AI is a retrieval-augmented generation (RAG) assistant for the built
environment. It helps construction companies, sustainability consultants,
bid/tender managers, developers, and design teams understand ESG topics,
analyse sustainability information, and produce ready-to-share documents — all
grounded in a curated knowledge base.

---

## What it does

- **Ask** plain-English questions about ESG, circular economy, embodied carbon,
  overheating/climate risk, and construction sustainability, and get answers
  grounded in the knowledge base.
- **Generate** ready-to-share drafts: executive summaries, ESG gap analyses,
  board briefings, tender checklists, action plans, LinkedIn posts, client
  emails, and presentation outlines.
- **Download** any generated document as a clean Markdown report.

All answers are drawn from a fixed, curated knowledge base so responses stay
focused and predictable. Generated content is always labelled as an AI draft
that should be reviewed before sharing.

---

## How it works

BuildLens AI is built on the LangChain + Streamlit RAG pattern:

1. **Knowledge base** — plain-text source files in `data/` covering ESG topics,
   circular economy, embodied carbon, UK home overheating risk, and practical
   recommendations. These are original summaries and analysis, not copyrighted
   reports.
2. **Retrieval** — `local_loader.py` loads the text files and `ensemble.py`
   builds an ensemble retriever (semantic + keyword) over them.
3. **Embeddings** — OpenAI `text-embedding-3-small`.
4. **Answer chain** — `full_chain.py` wraps the retriever in a RAG chain with an
   ESG-specialist system prompt that keeps answers grounded in retrieved
   sources.
5. **Generation prompts** — `prompts.py` defines the document templates used by
   the **Generate** tab.
6. **Reports** — `utils/report_generator.py` wraps generated text in a tidy
   Markdown report for download.
7. **UI** — `streamlit_app.py` provides a tabbed interface (Ask / Generate /
   Download) plus a short homepage overview.

---

## Project structure

```
streamlit_app.py          Main Streamlit app (UI + tabs)
full_chain.py             RAG chain and ESG system prompt
ensemble.py               Ensemble retriever setup
local_loader.py           Loads the text knowledge base
prompts.py                Document-generation prompt templates
utils/
  __init__.py
  report_generator.py     Builds the downloadable Markdown report
data/                     Curated ESG knowledge base (.txt)
```

---

## Running locally

You will need an OpenAI API key and a Hugging Face Hub token.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\\Scripts\\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Provide your keys (either as env vars or in .streamlit/secrets.toml)
export OPENAI_API_KEY="sk-..."
export HUGGINGFACEHUB_API_TOKEN="hf_..."

# 4. Run the app
streamlit run streamlit_app.py
```

You can also paste the keys into the sidebar when the app starts.

---

## Roadmap

Version 1 (this repo) uses a **fixed knowledge base**. Planned next steps,
best built and tested locally:

- Document upload (PDF / TXT / DOCX / CSV) with a document-type selector.
- An ESG scorecard across embodied carbon, circular economy, energy efficiency,
  climate resilience, social value, and supply chain transparency.
- Confidence labels (High / Medium / Low evidence) on answers.
- Project comparison and a richer dashboard snapshot.

---

## A note on sources and accuracy

The knowledge base is made of original summaries and analysis intended for
demonstration. BuildLens AI produces **AI-generated drafts**. Always review
output for accuracy before using it in tenders, board papers, or client work.

---

## Credits

Adapted from the `streamlit/example-app-langchain-rag` template and customised
for construction ESG use cases. Licensed under Apache-2.0.
