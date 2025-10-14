import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
import os
import json
from src.utils import is_valid_url, normalize_url


class Crawler:
    def __init__(self, start_url, max_pages=30, crawl_delay=1.5):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.crawl_delay = crawl_delay
        self.visited = set()
        self.data_dir = "data/crawled_pages"
        os.makedirs(self.data_dir, exist_ok=True)

    def crawl(self):
        to_visit = [self.start_url]
        page_count = 0
        skipped = 0

        while to_visit and page_count < self.max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue

            try:
                response = requests.get(url, timeout=10, headers={"User-Agent": "rag-crawler"})
                if response.status_code != 200:
                    skipped += 1
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
                clean_links = [normalize_url(l) for l in links if is_valid_url(l, self.domain)]

                filename = os.path.join(self.data_dir, f"page_{page_count}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump({"url": url, "content": text}, f, ensure_ascii=False, indent=2)

                page_count += 1
                self.visited.add(url)
                print(f"[{page_count}] Crawled: {url}")
                time.sleep(self.crawl_delay)

                for link in clean_links:
                    if link not in self.visited and len(to_visit) < self.max_pages:
                        to_visit.append(link)

            except Exception as e:
                print(f"❌ Error crawling {url}: {e}")
                skipped += 1

        return {"page_count": page_count, "skipped_count": skipped, "urls": list(self.visited)}


if __name__ == "__main__":
    crawler = Crawler("https://example.com", max_pages=10)
    print(crawler.crawl())
