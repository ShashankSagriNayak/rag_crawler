import time
from openai import OpenAI
from src.retriever import Retriever


class QAService:
    def __init__(self):
        self.client = OpenAI()
        self.retriever = Retriever()

    def build_prompt(self, question, retrieved):
        context = "\n\n".join([r["snippet"] for r in retrieved])
        return f"""
You are a helpful assistant that must answer strictly from the provided context.
If the context does not contain enough information, say exactly:
"Not found in crawled content."

Context:
{context}

Question: {question}
Answer:
"""

    def ask(self, question, top_k=3):
        start = time.time()
        retrieved = self.retriever.retrieve(question, top_k)
        retrieval_ms = int((time.time() - start) * 1000)

        prompt = self.build_prompt(question, retrieved)
        gen_start = time.time()

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content.strip()
        generation_ms = int((time.time() - gen_start) * 1000)

        total_ms = int((time.time() - start) * 1000)
        return {
            "answer": answer,
            "sources": [{"url": r["url"], "snippet": r["snippet"][:200]} for r in retrieved],
            "timings": {"retrieval_ms": retrieval_ms, "generation_ms": generation_ms, "total_ms": total_ms},
        }
