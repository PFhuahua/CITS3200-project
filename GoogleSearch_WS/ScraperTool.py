import re
import requests
from urllib.parse import urlparse, urljoin
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

def scrape_pdfs(url: str, filter_str: str = None, get_sizes: bool = True):
    """
    Scrape a webpage for PDF links.

    Args:
        url (str): The webpage URL to scrape.
        filter_str (str, optional): Only include PDFs containing this substring. Defaults to None.
        get_sizes (bool, optional): Whether to fetch Content-Length headers for sizes. Defaults to True.

    Returns:
        list[dict]: List of found PDFs, each as dict with keys:
            - 'url': Absolute URL to the PDF
            - 'filename': Filename extracted from the URL
            - 'size': Size in bytes (if available), otherwise None
    """
    # Parse base URL
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Get HTML content
    try:
        response = requests.get(url, headers=headers,  timeout=10)
        response.raise_for_status()
        html_content = response.text[:10000]

        print(f"Successfully fetched: {url}")
    except requests.exceptions.HTTPError as e:
        print(f" Skipped {url} due to HTTP error: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f" Skipped {url} due to timeout: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f" Skipped {url} due to request error: {e}")
        return None
    # Find PDF references
    pdf_refs = re.findall(r'href=["\'](.*?\.pdf(?:\?.*?)?)["\']', html_content, re.IGNORECASE)


    # Apply filter if given
    if filter_str:
        pdf_refs = [s for s in pdf_refs if filter_str in s]

    # Exclude unwanted matches (like file size placeholders)
    pdf_refs = [s for s in pdf_refs if "data-getfilesize=" not in s]

    # Normalize PDF links
    pdf_links = []
    for ref in pdf_refs:
        pdf_url = ref.replace('href="', '').replace('"', '')
        full_url = urljoin(base_url, pdf_url)
        filename = os.path.basename(full_url)

        size = None
        if get_sizes:
            try:
                head_resp = requests.head(full_url, allow_redirects=True, timeout=5)
                if 'Content-Length' in head_resp.headers:
                    size = int(head_resp.headers['Content-Length'])
            except requests.RequestException:
                size = None

        pdf_links.append({
            "url": full_url,
            "filename": filename,
            "size": size
        })

    return pdf_links
