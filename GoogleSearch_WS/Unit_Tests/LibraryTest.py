import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,scrape_Lib_Vis
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from SpecifiedLibraryFunc import scrape_library  # type: ignore

libsToCheck = ["France","Texas"]  #France, Texas
Search = "Census"
ResultsPerLib = 1

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
        "ResultSelector": "div.collapse-wrapper",
        "Visible": True
    },
    "Spain":{
        "Name": "National Library of Spain",
        "URL_Start": "https://catalogo.bne.es/discovery/search?query=any,contains,",
        "URL_End": "&tab=LibraryCatalog&search_scope=MyInstitution&vid=34BNE_INST:CATALOGO&lang=en&offset=0",
        "SearchSelector": "div.result-item-image layout-column"
    }
}


start = time.time()

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
