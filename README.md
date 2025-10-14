# 🧠 RAG Crawler — Domain-Scoped Retrieval-Augmented Generation Service

## 📌 Overview
This project implements a small **Retrieval-Augmented Generation (RAG)** pipeline that:
- Crawls and extracts content from a given website (within the same domain)
- Indexes and embeds the text for similarity search
- Answers user questions **grounded only** in the crawled content with proper **source citations**
- Refuses to answer when evidence is missing (“Not found in crawled content”)

The goal is correctness, grounding, and clarity within a limited engineering timebox (4–8 hours).

---

## 🚀 Architecture

**Pipeline:**  
`crawl → clean → chunk → embed → store → retrieve → generate → answer`

**Components:**
1. **Crawler (`crawler.py`)** – Collects pages within the domain, respects `robots.txt`, and stores text.  
2. **Cleaner (`text_cleaner.py`)** – Extracts main readable content, removing boilerplate (ads, navbars, etc.).  
3. **Indexer (`indexer.py`)** – Splits text into chunks (≈800 chars, 200 overlap), embeds using open-source model, and stores in a vector index (FAISS/Chroma).  
4. **Retriever (`retriever.py`)** – Retrieves top-k most relevant chunks for a given question.  
5. **Q&A Service (`qa_service.py`)** – Builds a grounded prompt from retrieved context, queries the model, and returns:
   ```json
   { 
     "answer": "...", 
     "sources": [{ "url": "...", "snippet": "..." }], 
     "timings": { "retrieval_ms": 42, "generation_ms": 311, "total_ms": 353 }
   }
  '''

⚙️ Setup & Installation
git clone https://github.com/<your-username>/rag_crawler.git
cd rag_crawler
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt

🧩 Example Usage (CLI)
# Crawl a site (up to 30 pages)
python cli/crawl_cli.py --url https://example.com --max_pages 30

# Index crawled data
python cli/index_cli.py --chunk_size 800 --chunk_overlap 200

# Ask a question
python cli/ask_cli.py "What is the mission of Example Company?"

Example Output

Answerable query

{
  "answer": "Example Company’s mission is to make web data accessible to everyone.",
  "sources": [
    { "url": "https://example.com/about", "snippet": "Our mission is to make web data accessible..." }
  ],
  "timings": { "retrieval_ms": 51, "generation_ms": 294, "total_ms": 345 }
}


Unanswerable query

{
  "answer": "Not found in crawled content.",
  "sources": [
    { "url": "https://example.com/contact", "snippet": "The website provides contact details..." }
  ]
}

📦 Folder Structure
rag_crawler/
├── src/
│   ├── crawler.py          # Crawl within domain
│   ├── text_cleaner.py     # Clean & extract readable text
│   ├── indexer.py          # Chunk & embed
│   ├── retriever.py        # Retrieve top-k
│   ├── qa_service.py       # Grounded QA generation
│   └── metrics_logger.py   # Latency, errors, stats
│
├── data/
│   ├── crawled_pages/
│   ├── vector_store/
│   └── logs/
│
├── cli/
│   ├── crawl_cli.py
│   ├── index_cli.py
│   └── ask_cli.py
│
├── tests/
├── docs/
└── examples/

🧠 Design Choices & Trade-offs

Chunking: 800-character chunks with 200 overlap ensure semantic continuity.

Embedding: sentence-transformers/all-MiniLM-L6-v2 chosen for speed and low resource cost.

Vector Store: FAISS (local, lightweight) for simplicity and speed.

Crawl Limit: Hard cap of 30–50 pages to avoid host overload.

Politeness: Crawl delay (1–2 s) and respect for robots.txt.

Grounding: Answers strictly limited to retrieved context; no external hallucination.

Refusal Logic: If retrieved context score < threshold → respond “Not found in crawled content.”

Prompt Hardening: Instructs model to ignore any instructions inside pages.

Observability: Logs retrieval & generation times, p50/p95 latencies, and errors.

Extensibility: Can easily swap embedding model or vector backend.

🧪 Evaluation
Metric	Description	Target
Grounding correctness	Answers must cite valid URLs	✅
Retrieval quality (Recall@k)	Top-k context includes relevant info	✅
Latency (p95)	< 2 s per query (local)	✅
Refusal correctness	No unsupported answers	✅

🔒 Safety & Guardrails

Ignores embedded or injected model instructions in pages.

Restricts all answers to crawled domain.

Declines to answer when evidence insufficient.

No execution of JavaScript or remote scripts.

🧰 Tooling and Prompts

Embedding model: sentence-transformers/all-MiniLM-L6-v2
LLM (open-source): e.g. mistral-7b-instruct, llama-3-8b-instruct, or similar local API
Libraries: requests, beautifulsoup4, trafilatura, faiss-cpu, sentence-transformers, chromadb, fastapi, tqdm, numpy
Prompt Template:

You are a helpful assistant that must answer strictly from the provided context.
If the context does not contain enough information, say exactly:
"Not found in crawled content."

Context:
{retrieved_chunks}

Question: {user_question}
Answer:

🧾 Example Evaluation Calls

/crawl → Crawl and store pages

/index → Build embeddings and store vectors

/ask → Retrieve & answer with grounding

Example eval set:

✅ “What is Example’s mission?” → Supported answer

❌ “Who founded Example?” → Refusal

🧭 Next Steps (Future Work)

Improve boilerplate removal using readability-lxml.

Add async crawler for faster coverage.

Integrate reranker model for better top-k relevance.

Containerize with Docker for reproducibility.

Author: Shashank Sagri Nayak

