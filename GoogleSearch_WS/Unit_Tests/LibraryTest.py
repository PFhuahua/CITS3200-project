import requests
from ScraperTool import scrape_Lib,Find_Lib_Results,scrape_Lib_Vis
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from SpecifiedLibraryFunc import scrape_library  # type: ignore

libsToCheck = ["France"] 
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
        "Result_URL_Start": "",
        "Visible": True,
        "CAPTCHA": False
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
        "Result_URL_Start": "",
        "Visible": True,
        "CAPTCHA": False
    },
    "Spain":{
        "Name": "National Library of Spain",
        "URL_Start": "https://catalogo.bne.es/discovery/search?query=any,contains,",
        "URL_End": "&tab=LibraryCatalog&search_scope=MyInstitution&vid=34BNE_INST:CATALOGO&lang=en&offset=0",
        "SearchSelector": "div.result-item-image",
        "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
        "tag": "h3",
        "tag_class": "item-title",
        "ResultSelector": "img.main-img",
        "Result_URL_Start": "",
        "Visible": True,
        "CAPTCHA": False
    },
    "Britian":{
        "Name": "British National Library",
        "URL_Start": "https://bll01.primo.exlibrisgroup.com/discovery/search?query=any,contains,",
        "URL_End": "&tab=LibraryCatalog&search_scope=Not_BL_Suppress&vid=44BL_INST:BLL01&lang=en&offset=0",
        "SearchSelector": "div.result-item-image",
        "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
        "tag": "h3",
        "tag_class": "item-title",
        "ResultSelector": "img.main-img",
        "Result_URL_Start": "",
        "Visible": True,
        "CAPTCHA": False
    },
    "Congress":{
        "Name": "LIBRARY OF CONGRESS",
        "URL_Start": "https://www.loc.gov/search/?in=&q=",
        "URL_End": "&new=true&st=",
        "SearchSelector": "div.iconic-container",
        "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
        "tag": "h3",
        "tag_class": "item-title",
        "ResultSelector": "img.main-img",
        "Result_URL_Start": "",
        "Visible": True,
        "CAPTCHA": True
    },
    "Germany":{
        "Name": "German National Library",
        "URL_Start": "https://portal.dnb.de/opac/simpleSearch?query=",
        "URL_End": " ",
        "SearchSelector": "td.number",
        "Attribute": {"id": re.compile(r"^recordLink_\d+$")},
        "tag": "table",
        "tag_class": "searchresult",
        "ResultSelector": 'img[alt="Neuigkeiten"]',
        "Result_URL_Start": "https://portal.dnb.de",
        "Visible": True,
        "CAPTCHA": False
    },
    "Netherlands":{
        "Name": "The National Library of the Netherlands",
        "URL_Start": "https://webggc.oclc.org/cbs/DB=2.37/CMD?ACT=SRCHA&IKT=1016&SRT=LST_Ya&TRM=",
        "URL_End": " ",
        "SearchSelector": "td.rec_mattype",
        "Attribute": {"class":"link_gen"},
        "tag": "td",
        "tag_class": "rec_title",
        "ResultSelector": 'td.rec_lable',
        "Result_URL_Start": "https://webggc.oclc.org/cbs/DB=2.37/SET=4/TTL=1/",
        "Visible": True,
        "CAPTCHA": False
    }
}


#for libs in Library: print(Library[libs]["Name"])
#for libs in Library: print(Library[libs]["Attribute"])

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
