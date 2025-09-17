import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,scrape_Lib_Vis # type: ignore
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

def scrape_library(Library, lib_name, Search, ResultsPerLib=5, max_workers=5):
    """
    Scrapes search results and detail pages for a given library.

    Args:
        Library (dict): Dictionary with scraping configuration for libraries.
        lib_name (str): The key in Library (e.g. "Texas", "France").
        Search (str): The search query.
        ResultsPerLib (int): How many results to keep per library.
        max_workers (int): Number of threads to run in parallel.

    Returns:
        list[str]: A list of HTML snippets (truncated to 1000 chars each).
    """
    HTMLS = [] 

    # Build query URL
    Query = Library[lib_name]["URL_Start"] + Search + Library[lib_name]["URL_End"]
    html_text = scrape_Lib(Query, Library[lib_name]["SearchSelector"])

    # Extract result links
    links = Find_Lib_Results(html_text,
                             Library[lib_name]["Attribute"],
                             Library[lib_name]["tag"],
                             Library[lib_name]["tag_class"])
    links = links[:ResultsPerLib]

    # Scraper wrapper for detail pages
    def scrape_wrapper(link):
        if Library[lib_name]["Visible"]:
            return link, scrape_Lib_Vis(link, Library[lib_name]["ResultSelector"])
        else:
            return link, scrape_Lib(link, Library[lib_name]["ResultSelector"])

    # Run scraping in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scrape_wrapper, link) for link in links]
        for future in as_completed(futures):
            link, Results_html = future.result()
            #print(link)
            #print(Results_html)
            #print(len(Results_html))
            if Results_html == None: continue
            HTMLS.append(Results_html[:1000])  # keep first 1000 chars

    return HTMLS
