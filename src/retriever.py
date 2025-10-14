import faiss
import numpy as np


class Retriever:
    def __init__(self, index_dir="data/vector_store"):
        self.index = faiss.read_index(f"{index_dir}/rag_index.faiss")
        self.metadata = np.load(f"{index_dir}/metadata.npy", allow_pickle=True)
        self.chunks = np.load(f"{index_dir}/chunks.npy", allow_pickle=True)
        from sentence_transformers import SentenceTransformer
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve(self, query, top_k=3):
        q_emb = self.embedder.encode([query])
        D, I = self.index.search(np.array(q_emb).astype("float32"), top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            results.append({"url": self.metadata[idx], "snippet": self.chunks[idx], "score": float(dist)})
        return results
