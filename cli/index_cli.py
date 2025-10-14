import argparse
import json
import time
from src.indexer import Indexer

def main():
    parser = argparse.ArgumentParser(description="Index crawled website pages into vector store.")
    parser.add_argument("--chunk_size", type=int, default=800, help="Chunk size for text splitting")
    parser.add_argument("--chunk_overlap", type=int, default=100, help="Overlap between text chunks")
    parser.add_argument("--embedding_model", default="all-MiniLM-L6-v2", help="Model for embeddings")

    args = parser.parse_args()

    print("🔧 Starting indexing...")
    start_time = time.time()

    result = Indexer().build_index(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        embedding_model=args.embedding_model
    )

    result["total_time_sec"] = round(time.time() - start_time, 2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
