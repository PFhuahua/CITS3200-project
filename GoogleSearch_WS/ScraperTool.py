import re
import requests
from urllib.parse import urlparse, urljoin
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

def process_pdf_link(full_url, get_sizes=True):
    """Process a single PDF URL to extract filename and optionally size."""
    filename = os.path.basename(full_url)
    size = None
    if get_sizes:
        try:
            head_resp = requests.head(full_url, allow_redirects=True, timeout=5)
            if 'Content-Length' in head_resp.headers:
                size = int(head_resp.headers['Content-Length'])
        except requests.RequestException:
            size = None
    return {
        "url": full_url,
        "filename": filename,
        "size": size
    }

def scrape_pdfs(url: str, filter_str: str = None, get_sizes: bool = True, max_time: int = 50):
    pdf_links = []

    def _scrape():
        # Parse base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Get HTML content
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text[:100000]
            print(len(html_content))
            print(f"Successfully fetched: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Skipped {url} due to request error: {e}")
            return pdf_links

        # Find PDF references
        pdf_refs = re.findall(r'href=["\']([^"\'>]+\.pdf(?:\?[^"\'>]*)?)["\']', html_content, re.IGNORECASE)

        # Apply filter if given
        if filter_str:
            pdf_refs = [s for s in pdf_refs if filter_str in s]

        # Exclude unwanted matches
        pdf_refs = [s for s in pdf_refs if "data-getfilesize=" not in s]

        # Process each PDF link using separate function
        for ref in pdf_refs:
            full_url = urljoin(base_url, ref)
            pdf_links.append(process_pdf_link(full_url, get_sizes=get_sizes))

        return pdf_links

    # Run scraper with total timeout
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_scrape)
        try:
            return future.result(timeout=max_time)
        except TimeoutError:
            print("Operation exceeded 50 seconds, returning partial results.")
            return pdf_links  # whatever was collected before timeout

