import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class Indexer:
    def __init__(self, chunk_size=800, chunk_overlap=200, embedding_model="all-MiniLM-L6-v2"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedder = SentenceTransformer(embedding_model)
        self.index_dir = "data/vector_store"
        os.makedirs(self.index_dir, exist_ok=True)

    def chunk_text(self, text):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def build_index(self,chunk_size=800, chunk_overlap=100,embedding_model="all-MiniLM-L6-v2"):
        all_chunks, metadata = [], []

        for file in os.listdir("data/crawled_pages"):
            path = os.path.join("data/crawled_pages", file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            chunks = self.chunk_text(data["content"])
            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append(data["url"])

        embeddings = self.embedder.encode(all_chunks, show_progress_bar=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings).astype("float32"))

        faiss.write_index(index, os.path.join(self.index_dir, "rag_index.faiss"))
        np.save(os.path.join(self.index_dir, "metadata.npy"), np.array(metadata))
        np.save(os.path.join(self.index_dir, "chunks.npy"), np.array(all_chunks))

        return {"vector_count": len(all_chunks), "errors": []}
