# 🏗 Construction ESG Research Assistant

An AI-powered research assistant for ESG, circular economy, embodied carbon, overheating risk, and sustainability in the built environment.

Built with Streamlit, LangChain, OpenAI embeddings, and retrieval-augmented generation.

---

## What it does

This app allows users to ask plain-English questions about sustainable construction and receive clear, context-grounded answers from a curated knowledge base.

**Example questions:**
- What are the most important ESG topics in construction?
- What is embodied carbon?
- How can UK homes reduce overheating risk?
- What does circular economy mean in construction?
- What practical actions can construction firms take to improve ESG performance?

---

## Why I built it

Construction professionals are under pressure to understand ESG, climate risk, carbon reduction, overheating, and circular economy principles. Important information is often spread across long reports and technical documents.

This project shows how retrieval-augmented generation can make specialist knowledge easier to access and understand, especially for professionals who need fast, practical answers.

---

## Tech stack

- **Python** — core language
- **Streamlit** — web app interface and chat UI
- **LangChain** — orchestration of retrieval and generation
- **OpenAI embeddings** — text-embedding-3-small for semantic search
- **BM25 retrieval** — keyword-based search
- **Ensemble retriever** — combines BM25 and vector search with equal weights
- **ChromaDB / vector store** — stores document embeddings

---

## Responsible AI features

- Answers are grounded in a curated knowledge base on ESG and construction
- The assistant is explicitly instructed not to invent facts, regulations, numbers, or citations
- The app explains when there is not enough evidence to answer confidently
- Users are informed the app answers from a limited curated knowledge base
- Future version will add source-level citations and answer quality evaluation

---

## Knowledge base

The app is powered by 5 curated knowledge files covering:

| File | Topic |
|------|-------|
| `esg_construction_topics.txt` | Overview of ESG themes: environmental, social, governance |
| `embodied_carbon_basics.txt` | What embodied carbon is, how to measure and reduce it |
| `uk_home_overheating_risk.txt` | Causes, risks, design strategies, and UK policy context |
| `circular_economy_construction.txt` | Circular economy principles, material passports, design for disassembly |
| `practical_recommendations.txt` | Actionable ESG steps for construction companies |

All content is original analysis and summary based on publicly available knowledge. No copyrighted reports are included.

---

## Architecture

```
User question
     ↓
Streamlit chat interface
     ↓
Ensemble Retriever
     ↓
BM25 keyword search + vector similarity search (equal weights)
     ↓
Relevant document chunks from knowledge base
     ↓
LLM (GPT) with ESG specialist system prompt
     ↓
Grounded plain-English answer
     ↓
User
```

---

## How to run locally

```bash
git clone https://github.com/yenlikgaisina/construction-esg-rag-assistant.git
cd construction-esg-rag-assistant

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

streamlit run streamlit_app.py
```

You will need:
- An **OpenAI API key** — enter it in the sidebar when the app loads
- A **HuggingFace Hub API token** — enter it in the sidebar when the app loads

Or set them in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key"
HUGGINGFACEHUB_API_TOKEN = "your-token"
```

---

## Deployment

This app is designed to be deployed on **Streamlit Community Cloud**:

1. Push your fork to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** and select this repository
4. Set main file path to `streamlit_app.py`
5. Add secrets in the Streamlit Cloud dashboard

---

## Future improvements

- [ ] Add PDF upload so users can ask questions over their own documents
- [ ] Add source citations in answers (show which file each answer came from)
- [ ] Add answer quality evaluation and hallucination detection
- [ ] Add ESG topic filters for more focused search
- [ ] Add downloadable answer summaries
- [ ] Expand the knowledge base with more ESG construction topics

---

## About

Built by [Yenlik Gaisina](https://github.com/yenlikgaisina) as part of a portfolio of AI and data projects focused on ESG, sustainability, and the built environment.

Forked from [streamlit/example-app-langchain-rag](https://github.com/streamlit/example-app-langchain-rag) and significantly customised.
