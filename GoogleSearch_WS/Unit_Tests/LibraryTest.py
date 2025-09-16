import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,scrape_Lib_Vis # type: ignore
import time

Search = "Census"


api_key = "API KEY" #API KEY
Searchcx = "97c19d00f487341b6"

Library = {
    "Texas":{
    "Name": "Texas",
    "URL_Start": "https://search.lib.utexas.edu/discovery/search?query=any,contains,",
    "URL_End": "&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
    "SearchSelector": "div.result-item-image",
    "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
    "ResultSelector": "div.bar.alert-bar",
    "Visible": True
    }
    }


start = time.time()
Query = Library["Texas"]["URL_Start"] + Search + Library["Texas"]["URL_End"]
html_text = scrape_Lib(Query,Library["Texas"]["SearchSelector"])
links = Find_Lib_Results(html_text,Library["Texas"]["Attribute"])
for link in links:
    print(link)
    if Library["Texas"]["Visible"]:
        Results_html = scrape_Lib_Vis(link,Library["Texas"]["ResultSelector"])
    else:
        Results_html = scrape_Lib(link,Library["Texas"]["ResultSelector"])
    print(Results_html)
    print(len(Results_html))

end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
