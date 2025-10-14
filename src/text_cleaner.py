import trafilatura

def extract_clean_text(html_content: str) -> str:
    """Extract readable main content from HTML using Trafilatura."""
    clean_text = trafilatura.extract(html_content, include_comments=False, include_links=False)
    return clean_text or ""
