import argparse
import json
import time
from src.qa_service import ask_question

def main():
    parser = argparse.ArgumentParser(description="Ask questions grounded in crawled website data.")
    parser.add_argument("--question", required=True, help="Question to ask about the crawled website")
    parser.add_argument("--top_k", type=int, default=3, help="Number of top retrieved chunks for context")

    args = parser.parse_args()

    print(f"🤖 Answering question: '{args.question}'")
    start_time = time.time()

    response = ask_question(
        question=args.question,
        top_k=args.top_k
    )

    response["timings"]["total_ms"] = round((time.time() - start_time) * 1000, 2)
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
