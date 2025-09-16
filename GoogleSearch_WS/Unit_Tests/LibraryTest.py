import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,GetHTML # type: ignore
import time


api_key = "" #API KEY
Searchcx = "97c19d00f487341b6"

Library = {
    "Texas":{
    "Name": "Texas",
    "URL": "https://search.lib.utexas.edu/discovery/search?query=any,contains,census&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
    "SearchSelector": "div.result-item-image",
    "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
    "ResultSelector": "img.main-img",
    }
    }


start = time.time()
html_text = scrape_Lib(Library["Texas"]["URL"],Library["Texas"]["SearchSelector"])
links = Find_Lib_Results(html_text,Library["Texas"]["Attribute"])
for link in links:
    print(link)
    Results_html = scrape_Lib(link,Library["Texas"]["SearchSelector"])
    print(len(Results_html))

end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
