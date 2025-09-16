import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,scrape_Lib_Vis # type: ignore
import time
from concurrent.futures import ThreadPoolExecutor, as_completed



libsToCheck = ["France", "Texas"]  #France, Texas
Search = "Census"
ResultsPerLib = 5

api_key = "API" #API KEY
Searchcx = "97c19d00f487341b6"

Library = {
    "Texas":{
    "Name": "University of Texas Libraries",
    "URL_Start": "https://search.lib.utexas.edu/discovery/search?query=any,contains,",
    "URL_End": "&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
    "SearchSelector": "div.result-item-image",
    "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
    "tag": "h3",
    "tag_class": "item-title",
    "ResultSelector": "div.bar.alert-bar",
    "Visible": True
    },
    "France":{
    "Name": "National Library of France",
    "URL_Start": "https://data.bnf.fr/search?term=",
    "URL_End": " ",
    "SearchSelector": "div.itemlist-item",
    "Attribute": {"itemprop": "name"},
    "tag": "div",
    "tag_class": "itemlist-item",
    "ResultSelector": "div.bar.alert-bar",
    "Visible": True
    }
    }

start = time.time()

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
            print(len(Results_html))
            HTMLS.append(Results_html[:1000])  # keep first 1000 chars

    return HTMLS


with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {
        executor.submit(scrape_library, Library, lib, Search, ResultsPerLib): lib
        for lib in libsToCheck
    }

    results = {}
    for future in as_completed(futures):
        lib_name = futures[future]
        try:
            results[lib_name] = future.result()
        except Exception as e:
            print(f"{lib_name} failed: {e}")
    print(results)



end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
