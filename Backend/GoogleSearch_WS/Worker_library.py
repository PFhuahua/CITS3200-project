import requests
from .ScraperTool import Scrape_Page,Hyperlink_Extractor # type: ignore
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def scrape_library(Library, lib_name, Search, ResultsPerLib=5, max_workers=5, timeout= 15000):
    """
    Scrapes search results and detail pages for a given library.

    Args:
        Library (dict): Dictionary with scraping configuration for libraries.
        lib_name (str): The key in Library (e.g. "Texas", "France").
        Search (str): The search query.
        ResultsPerLib (int): How many results to keep per library.
        max_workers (int): Number of threads to run in parallel.
        timeout (int): Maximum time (ms, 1000ms = 1sec) to wait for a page to load.

    Returns:
        list[str]: A list of HTML extracted and filtered for text.
    """
    HTMLS = []

    # Build query URL
    Query = Library[lib_name]["URL_Start"] + Search + Library[lib_name]["URL_End"]
    html_text = Scrape_Page(Query, Library[lib_name]["SearchSelector"],timeout = timeout)

    # Extract result links
    links = Hyperlink_Extractor(html_text,
                             Library[lib_name]["Attribute"],
                             Library[lib_name]["tag"],
                             Library[lib_name]["tag_class"])
    links = [Library[lib_name]["Result_URL_Start"] + link for link in links[:ResultsPerLib]]

    # Scraper wrapper for detail pages
    def scrape_wrapper(link):
        if Library[lib_name]["Visible"]:
            return link, Scrape_Page(link, Library[lib_name]["ResultSelector"], visible = True,timeout = timeout)
        else:
            return link, Scrape_Page(link, Library[lib_name]["ResultSelector"],timeout = timeout)

    # Run scraping in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_wrapper, link) for link in links]
        for future in as_completed(futures):
            link, Results_html = future.result()

            if Results_html == None: continue
            soup = BeautifulSoup(Results_html, "html.parser")

            for script_or_style in soup(["script", "style", "noscript"]):
                script_or_style.decompose()

            # Get text
            text = soup.get_text(separator=" ")
            body_content = re.sub(r"\s+", " ", text).strip()
            HTMLS.append([link,body_content])

    return HTMLS
