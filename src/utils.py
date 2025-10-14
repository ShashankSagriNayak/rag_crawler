from urllib.parse import urlparse


def is_valid_url(url, domain):
    parsed = urlparse(url)
    return bool(parsed.netloc) and domain in parsed.netloc and parsed.scheme in ["http", "https"]


def normalize_url(url):
    return url.split("#")[0].rstrip("/")
