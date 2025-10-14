import argparse
import json
import time
from src.crawler import crawl_website

def main():
    parser = argparse.ArgumentParser(description="Crawl a website within domain limits.")
    parser.add_argument("--start_url", required=True, help="Starting URL to begin crawl")
    parser.add_argument("--max_pages", type=int, default=30, help="Maximum number of pages to crawl")
    parser.add_argument("--max_depth", type=int, default=2, help="Maximum crawl depth")
    parser.add_argument("--crawl_delay_ms", type=int, default=1000, help="Delay between requests in ms")

    args = parser.parse_args()

    print(f"🚀 Starting crawl: {args.start_url}")
    start_time = time.time()

    result = crawl_website(
        start_url=args.start_url,
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        crawl_delay_ms=args.crawl_delay_ms
    )

    result["total_time_sec"] = round(time.time() - start_time, 2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
