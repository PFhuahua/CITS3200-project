import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from Worker_library import scrape_library  # type: ignore

def Find_Lib_Results(Query, SpecifiedLibs: list[str] = None, NumResults: int = 1, max_workers: int = 9, timeout= 15000):
    """
    Uses Search Feature on National libraries simultaneously using a given query.
    
    Args:
        Query (str): The search queried directly to libraries.

        SpecifiedLibs (list[str]): Additional library sources to include in the search. 

        NumResults (int, optional): The number of top results scraped and outputted per library search. Default is 2.

        max_workers (int, optional): The maximum number of concurrent threads used. Defaults to 6.

        timeout (int): Maximum time (ms, 1000ms = 1sec) to wait for a page to load.

    Returns:
        dict: A dictionary mapping each library name to a list of result links and visible text extracted. 

    Notes:
        - The function always calls a set of priority libraries ontop of those specified in the parameter.
        - If a library search fails or finds no result to scrape the dict entry defaults to [], and execution continues.
    """
    libsToCheck = ["Texas","France","Spain","Britian","Germany","Netherlands","Portugal","Canada","London","United States","National Archives","South Africa"] 
    ResultsPerLib = NumResults
    Search = Query

    # Merge List of always search libs and specified libs 
    if (SpecifiedLibs != None):  libsToCheck = list(set(libsToCheck + SpecifiedLibs))


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
        },
        "Portugal":{
            "Name": "National Library of Portugal",
            "URL_Start": "https://bndigital.bnportugal.gov.pt/records?navigation=default&perpage=10&page=1&search=",
            "URL_End": "&fulltext=1&child=1&bookmarks=1&sort=_score#page",
            "SearchSelector": "div.navlist_img",
            "Attribute": {},
            "tag": "div",
            "tag_class": "navlist_content",
            "ResultSelector": 'img.scale-with-grid',
            "Result_URL_Start": "https://bndigital.bnportugal.gov.pt",
            "Visible": True,
            "CAPTCHA": False
        },
        "Canada":{
            "Name": "Canada Government Collection",
            "URL_Start": "https://recherche-collection-search.bac-lac.gc.ca/eng/Home/Result?q_type_1=q&q_1=",
            "URL_End": "&SEARCH_TYPE=SEARCH_BASIC&",
            "SearchSelector": "img.lazyloaded",
            "Attribute": {"onclick":"SaveTopScrollPosition()"},
            "tag": "div",
            "tag_class": "CFCS-width-all",
            "ResultSelector": 'div.ucc-container',
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "London":{
            "Name": "London School of Economics and Political Science",
            "URL_Start": "https://librarysearch.lse.ac.uk/discovery/search?query=any,contains,",
            "URL_End": "&tab=Everything&search_scope=MyInst_and_CI&vid=44LSE_INST:44LSE_VU1&offset=0",
            "SearchSelector": "img.main-img",
            "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
            "tag": "h3",
            "tag_class": "item-title",
            "ResultSelector": "img.main-img",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "United States":{
            "Name": "United States Census Bureau",
            "URL_Start": "https://www.census.gov/search-results.html?q=",
            "URL_End": "&page=1&stateGeo=none&searchtype=web&cssp=SERP&_charset_=UTF-8",
            "SearchSelector": "div.uscb-search-result__page-snippet",
            "Attribute": {"onclick":"searchCustomEvent('ORG:https:\/\/www.census.gov\/about\/history\/bureau\\u002Dhistory\/census\\u002Dpeople\/census\\u002Ddirectors.html'"},
            "tag": "div",
            "tag_class": "search-results",
            "ResultSelector": "img.main-img",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "National Archives":{
            "Name": "United States National Archives",
            "URL_Start": "https://search.archives.gov/search?affiliate=national-archives&query=",
            "URL_End": "",
            "SearchSelector": "img.usa-identifier__logo",
            "Attribute": {"class": "result-title-link"},
            "tag": "div",
            "tag_class": "search-result-item-wrapper",
            "ResultSelector": "body.html",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "South Africa":{
            "Name": "National Library of South Africa (NLSA)",
            "URL_Start": "https://cdm21048.contentdm.oclc.org/digital/search/searchterm/",
            "URL_End": "",
            "SearchSelector": "img.SearchResult-thumbnail",
            "Attribute": {"tabindex": "0"},
            "tag": "div",
            "tag_class": "Search-mainContent",
            "ResultSelector": "div.ItemPDF-itemImage",
            "Result_URL_Start": "https://cdm21048.contentdm.oclc.org",
            "Visible": True,
            "CAPTCHA": False
        },#END OF PRIORITY NOW IN ALPHABETICAL https://www.flagpictures.com/countries/national-libraries/?utm_source=chatgpt.com%5C
        "Afghanistan":{
            "Name":"Afghanistan Center at Kabul University",
            "URL_Start": "https://archive.af/cgi-bin/koha/opac-search.pl?q=",
            "URL_End": "",
            "SearchSelector": "div.title_summary",
            "Attribute": {"class": "title"},
            "tag": "div",
            "tag_class": "title_summary",
            "ResultSelector": "td.itype",
            "Result_URL_Start": "https://archive.af",
            "Visible": True,
            "CAPTCHA": False
        },
        "Albania":{
            "Name": "National Library of Albania",
            "URL_Start": "https://www.bksh.al/search/",
            "URL_End": "",
            "SearchSelector": "div.record-image",
            "Attribute": {},
            "tag": "div",
            "tag_class": "katalogu-materiale",
            "ResultSelector": "h2.text-primary",
            "Result_URL_Start": "https://www.bksh.al",
            "Visible": True,
            "CAPTCHA": False
        }
    }


    #for libs in Library: print(Library[libs]["Name"])
    #for libs in Library: print(Library[libs]["Attribute"])

    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(scrape_library, Library, lib, Search, ResultsPerLib,timeout = timeout): lib
            for lib in libsToCheck
        }

        results = {}
        for future in as_completed(futures):
            lib_name = futures[future]
            try:
                results[lib_name] = future.result()
            except Exception as e:
                print(f"{lib_name} failed: {e}")
        for key, value in results.items():
            for v in value:
                print(key, v[0])



    end = time.time()
    #print(f"Elapsed time: {end - start:.4f} seconds")
    return(results)


def Find_Bur_Results(Query, SpecifiedLibs: list[str] = None, NumResults: int = 1, max_workers: int = 9, timeout= 15000):
    """
    Uses Search Feature on National Bureaus simultaneously using a given query.
    
    Args:
        Query (str): The search queried directly to bureaus.

        SpecifiedLibs (list[str]): Additional bureau sources to include in the search. 

        NumResults (int, optional): The number of top results scraped and outputted per bureau search. Default is 2.

        max_workers (int, optional): The maximum number of concurrent threads used. Defaults to 6.

        timeout (int): Maximum time (ms, 1000ms = 1sec) to wait for a page to load.

    Returns:
        dict: A dictionary mapping each bureau name to a list of result links and visible text extracted. 

    Notes:
        - The function always calls a set of priority bureau ontop of those specified in the parameter.
        - If a bureau search fails or finds no result to scrape the dict entry defaults to [], and execution continues.
    """
    libsToCheck = ["France"] 
    ResultsPerLib = NumResults
    Search = Query

    # Merge List of libs to always search and specified libs 
    if (SpecifiedLibs != None):  libsToCheck = list(set(libsToCheck + SpecifiedLibs))

    #https://unstats.un.org/home/nso_sites/ France
    Library = {
        "France":{
            "Name": "France National Institute of Statistics and Economic Studies",
            "URL_Start": "https://www.insee.fr/fr/recherche?idprec=8226711&q=",
            "URL_End": "&debut=0",
            "SearchSelector": "div.echo-chapo",
            "Attribute": {"class": "echo-lien"},
            "tag": "tr",
            "tag_class": "cliquable",
            "ResultSelector": "span.hidden-template-impression",
            "Result_URL_Start": "https://www.insee.fr",
            "Visible": True,
            "CAPTCHA": False
        }
    }

    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(scrape_library, Library, lib, Search, ResultsPerLib,timeout = timeout): lib
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
    #print(f"Elapsed time: {end - start:.4f} seconds")
    return(results)

