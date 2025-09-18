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
    #print(f"Processing {full_url}")
    filename = os.path.basename(full_url)
    size = None
    content_type = None
    if get_sizes:
        try:
            head_resp = requests.head(full_url, allow_redirects=True, timeout=5)
            #print(f"\n{filename}\n{full_url}\n{head_resp.headers}\n")
            content_type = head_resp.headers.get("Content-Type", "").lower()

            # 404 PDF not found
            if content_type == "text/html; charset=utf-8":
                return None
            
            # File Size
            if 'Content-Length' in head_resp.headers:
                size = round(int(head_resp.headers['Content-Length'])/1000,0) #PDF size in KB
        except requests.RequestException:
            size = None
            content_type = None
    return {
        "url": full_url,
        "filename": filename,
        "size": size,
        "filetype": content_type
    }

def scrape_pdfs(url: str, filter_str: str = None, get_sizes: bool = True, max_time: int = 40, MaxPDFperPage = 4):
    pdf_links = []

    def _scrape():
        # Parse base URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Get HTML content
        try:
            #print(f"fetching: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            html_content = response.text
            # Process HTML in chunks for effeciency
            chunk_size = 1024
            pdf_refs = []
            for i in range(0, len(html_content), chunk_size):
                chunk = html_content[i:i+chunk_size]
                pdf_refs.extend(
                    re.findall(r'href=["\']([^"\'>]+\.pdf(?:\?[^"\'>]*)?)["\']',
                            chunk, re.IGNORECASE)
                )
                if len(pdf_refs) > MaxPDFperPage: break
            #print(len(html_content))
            #print(f"Successfully fetched: {url}, PDFs Found: {len(pdf_refs)}")
        except requests.exceptions.RequestException as e:
            #print(f"Skipped {url} due to request error: {e}")
            return pdf_links

        # Apply filter if given
        if filter_str:
            pdf_refs = [s for s in pdf_refs if filter_str in s]

        # Exclude unwanted matches
        pdf_refs = [s for s in pdf_refs if "data-getfilesize=" not in s]

        # Process each PDF link using separate function
        for ref in pdf_refs:
            full_url = urljoin(base_url, ref)
            pdf_info = process_pdf_link(full_url, get_sizes=get_sizes)
            if pdf_info != None:
                pdf_links.append(pdf_info)
                print("PDF added")

        return pdf_links

    # Run scraper with total timeout
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_scrape)
        try:
            return future.result(timeout=max_time)
        except TimeoutError:
            print("Operation exceeded 40 seconds, returning partial results.")
            return pdf_links  # whatever was collected before timeout

def GetHTML(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

def scrape_Lib(url: str,selector: str):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True means no window opens
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(selector)  # wait for results
        html = page.content()  # get fully rendered HTML
        browser.close()
        return(html)


def Find_Lib_Results(html,attrs):

    soup = BeautifulSoup(html, "html.parser")

    # find <h3 class="item-title">, then get <a> inside it
    links = []
    for h3 in soup.find_all("h3", class_="item-title"):
        a = h3.find("a", attrs=attrs)
        if a and a.has_attr("href"):
            links.append(a["href"])

    return(links)
