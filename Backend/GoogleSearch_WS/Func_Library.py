import requests
import time,os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from Worker_library import scrape_library  # type: ignore

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from Backend.db.db import SessionLocal
from Backend.db.models import Library as LibraryModel, Bureau as BureauModel

def integrate_db_call():
    session = SessionLocal()
  
    try:
        library_dict = {}
        bureau_dict = {}

        libraries = session.query(LibraryModel).all()
        for lib in libraries:
            country = getattr(lib, "country", None)
            if not country:
                continue
            library_dict[country] = {
                "id": lib.id,
                "name": lib.name,
                "URL_Start": lib.url_start,
                "URL_End": lib.url_end,
                "Result_URL_Start": lib.result_url_start,
                "SearchSelector": lib.search_selector,
                "Attribute": lib.attribute,
                "tag": lib.tag,
                "tag_class": lib.tag_class,
                "ResultSelector": lib.result_selector,
                "Visible": lib.visible,
                "priority": lib.priority,
                "CAPTCHA": lib.captcha,
            }

        bureaus = session.query(BureauModel).all()
        for bur in bureaus:
            country = getattr(bur, "country", None)
            if not country:
                continue
            bureau_dict[country] = {
                "id": bur.id,
                "name": bur.name,
                "URL_Start": bur.url_start,
                "URL_End": bur.url_end,
                "Result_URL_Start": bur.result_url_start,
                "SearchSelector": bur.search_selector,
                "Attribute": bur.attribute,
                "tag": bur.tag,
                "tag_class": bur.tag_class,
                "ResultSelector": bur.result_selector,
                "Visible": bur.visible,
                "priority": bur.priority,
                "CAPTCHA": bur.captcha,
            }
        return library_dict, bureau_dict

    finally:
        session.close()

class DBBackedLibrary(dict):
    def __getitem__(self, country_name):
        session = SessionLocal()
        try:
            results = session.query(LibraryModel).filter_by(country=country_name).all()
            if not results:
                raise KeyError(f"No library found for {country_name}")
            r = results[0] 
            return {
                    "id": r.id,
                    "Name": r.name,
                    "URL_Start": r.url_start,
                    "URL_End": r.url_end,
                    "Result_URL_Start": r.result_url_start,
                    "SearchSelector": r.search_selector,
                    "Attribute": r.attribute,
                    "tag": r.tag,
                    "tag_class": r.tag_class,
                    "ResultSelector": r.result_selector,
                    "Visible": r.visible,
                    "priority": r.priority,
                    "CAPTCHA": r.captcha,
            }
        finally:
            session.close()
class DBBackedBureau(dict):
    def __getitem__(self, country_name):
        session = SessionLocal()
        try:
            results = session.query(BureauModel).filter_by(country=country_name).all()
            if not results:
                raise KeyError(f"No bureau found for {country_name}")
            r = results[0] 
            return{ 
                    "id": r.id,
                    "Name": r.name,
                    "URL_Start": r.url_start,
                    "URL_End": r.url_end,
                    "Result_URL_Start": r.result_url_start,
                    "SearchSelector": r.search_selector,
                    "Attribute": r.attribute,
                    "tag": r.tag,
                    "tag_class": r.tag_class,
                    "ResultSelector": r.result_selector,
                    "Visible": r.visible,
                    "priority": r.priority,
                    "country": r.country,
                    "CAPTCHA": r.captcha,
                }
        finally:
            session.close()


# Instantiate the DB-backed dictionaries
Library = DBBackedLibrary()
Bureau = DBBackedBureau()


def Find_Lib_Results(Query, SpecifiedLibs: list[str] = None, NumResults: int = 2, max_workers: int = 9, timeout= 15000):
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
    libsToCheck = ["Texas","France","Spain","Britian","Germany","Netherlands","Portugal","Canada","London","National Archives","South Africa"] 
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
        },
        "Aruba":{
            "Name": "Aruba National Library",
            "URL_Start": "https://bibliotecanacional.on.worldcat.org/search?queryString=",
            "URL_End": " ",
            "SearchSelector": "div.cssltr-110i50s",
            "Attribute": {"class": "MuiTypography-root MuiTypography-body1 MuiLink-root MuiLink-underlineAlways cssltr-9mpld1"},
            "tag": "div",
            "tag_class": "MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation4 jss198 cssltr-110i50s",
            "ResultSelector": "div.jss138",
            "Result_URL_Start": "https://bibliotecanacional.on.worldcat.org",
            "Visible": True,
            "CAPTCHA": False
        },
        "Australia":{
            "Name": "National Library of Australia",
            "URL_Start": "https://catalogue.nla.gov.au/search?q=",
            "URL_End": " ",
            "SearchSelector": "div.col",
            "Attribute": {},
            "tag": "h3",
            "tag_class": "bento-item-title col-12",
            "ResultSelector": "div.document-main-section",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Austria":{
            "Name": "Austrian National Library",
            "URL_Start": "https://search.onb.ac.at/primo-explore/search?institution=43ACC_ONB&vid=ONB&tab=default_tab&search_scope=ONB_gesamtbestand&mode=basic&displayMode=full&bulkSize=10&highlight=true&dum=true&displayField=all&query=any,contains,",
            "URL_End": " ",
            "SearchSelector": "div.result-item-image",
            "Attribute": {"ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"},
            "tag": "h3",
            "tag_class": "item-title",
            "ResultSelector": "img.main-img",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Azerbaijan":{
            "Name": "Akhundov National Library",
            "URL_Start": "https://ek.anl.az/search/query?term_1=",
            "URL_End": "&locale=az&theme=e-kataloq",
            "SearchSelector": "div.formatImage",
            "Attribute": {"class": "title"},
            "tag": "div",
            "tag_class": "record",
            "ResultSelector": "img.main-img",
            "Result_URL_Start": "https://ek.anl.az",
            "Visible": True,
            "CAPTCHA": False
        },
        "Bahamas" :{
            "Name": "Bahamas National Library",
            "URL_Start": "https://nlis.goalexandria.com/search?search=(((title%3A%3A",
            "URL_End": "))%20%26%26%20(hidetitle%3A%3A0))",
            "SearchSelector": "div.item-picture",
            "Attribute": {},
            "tag": "div",
            "tag_class": "item-container",
            "ResultSelector": "div.item-picture",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Belgium" :{ # Belgium Takes a long time to load 
            "Name": "Royal Library of Belgium",
            "URL_Start": "https://opac.kbr.be/Library/search.aspx?SC=KBR_UNIFIED&QUERY=",
            "URL_End": "&_lg=en-GB",
            "SearchSelector": "img.img-thumbnail ermes-thumb ermes-thumb-size-MEDIUM",
            "Attribute": {},
            "tag": "div",
            "tag_class": "vignette_container",
            "ResultSelector": "mg.img-thumbnail ermes-thumb ermes-thumb-size-MEDIUM",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Belize" :{ 
            "Name": "Belize National Library Service and Information System",
            "URL_Start": "https://dloc.com/collections/inlsbze/results?q=",
            "URL_End": "",
            "SearchSelector": "div.BriefView_image__NZDFL",
            "Attribute": {"class" : "image-link"},
            "tag": "article",
            "tag_class": "BriefView_container__MMnuA BriefView_lg__iDdkG",
            "ResultSelector": "div.text-center order-1 order-xl-2 mt-4 col-xl-4 col-12",
            "Result_URL_Start": "https://dloc.com",
            "Visible": True,
            "CAPTCHA": False
        },
        "Bolivia" :{ 
            "Name": "National Archive and Library of Bolivia",
            "URL_Start": "https://archivo-abnb.org.bo/index.php/informationobject/browse?topLod=0&query=",
            "URL_End": "",
            "SearchSelector": "p.title",
            "Attribute": {},
            "tag": "p",
            "tag_class": "title",
            "ResultSelector": "li.treeitem",
            "Result_URL_Start": "https://archivo-abnb.org.bo",
            "Visible": True,
            "CAPTCHA": False
        },
        "Bosnia And Herzegovina" :{ 
            "Name": "National and University Library of Bosnia and Herzegovina",
            "URL_Start": "https://plus.cobiss.net/cobiss/bh/bs/bib/search?q=",
            "URL_End": "",
            "SearchSelector": "div.txtCenter",
            "Attribute": {"class":"title value"},
            "tag": "div",
            "tag_class": "message",
            "ResultSelector": "i.icon-1",
            "Result_URL_Start": "https://plus.cobiss.net/cobiss/bh/bs/",
            "Visible": True,
            "CAPTCHA": False
        },
        "Bulgaria" :{ 
            "Name": "SS. Cyril and Methodius National Library",
            "URL_Start": "https://plus.cobiss.net/cobiss/bg/bg/bib/search?q=",
            "URL_End": "",
            "SearchSelector": "div.txtCenter",
            "Attribute": {"class":"title value"},
            "tag": "div",
            "tag_class": "message",
            "ResultSelector": "i.icon-1",
            "Result_URL_Start": "https://plus.cobiss.net/cobiss/bg/bg/",
            "Visible": True,
            "CAPTCHA": False
        },
        "Cabo Verde" :{ 
            "Name": "BIBLIOTECA NACIONAL DE CABO VERDE",
            "URL_Start": "http://catalogo.bn.cv/cgi-bin/koha/opac-search.pl?idx=&q=",
            "URL_End": "",
            "SearchSelector": "div.results_summary",
            "Attribute": {"class":"title"},
            "tag": "div",
            "tag_class": "title_summary",
            "ResultSelector": "div.toptabs",
            "Result_URL_Start": "http://catalogo.bn.cv",
            "Visible": True,
            "CAPTCHA": False
        },
        "Cabo Verde" :{ 
            "Name": "BIBLIOTECA NACIONAL DE CABO VERDE",
            "URL_Start": "http://catalogo.bn.cv/cgi-bin/koha/opac-search.pl?idx=&q=",
            "URL_End": "",
            "SearchSelector": "div.results_summary",
            "Attribute": {"class":"title"},
            "tag": "div",
            "tag_class": "title_summary",
            "ResultSelector": "div.toptabs",
            "Result_URL_Start": "http://catalogo.bn.cv",
            "Visible": True,
            "CAPTCHA": False
        },
        "Chile" :{ 
            "Name": "BIBLIOTECA NACIONAL DE CABO VERDE",
            "URL_Start": "http://descubre.bibliotecanacional.gob.cl/primo-explore/search?query=any,contains,",
            "URL_End": "&tab=bnc_tab&search_scope=bnc_completo&vid=BNC&offset=0",
            "SearchSelector": "img.main-img",
            "Attribute": {"ng-class":"::{'full-view-mouse-pointer':$ctrl.isFullView}"},
            "tag": "h3",
            "tag_class": "item-title",
            "ResultSelector": "img.main-img",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Colombia" :{ 
            "Name": "National Library of Colombia",
            "URL_Start": "https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/results?qu=",
            "URL_End":  "",
            "SearchSelector": "img.results_img",
            "Attribute": {"class": "detailLink text-h3"},
            "tag": "div",
            "tag_class": "stupid_ie_div",
            "ResultSelector": "div.no_image_text",
            "Result_URL_Start": "https://catalogoenlinea.bibliotecanacional.gov.co/",
            "Visible": True,
            "CAPTCHA": False
        },
        "Croatia" :{ 
            "Name": "National and University Library Zagreb",
            "URL_Start": "https://digitalna.nsk.hr/?pr=l&msq=",
            "URL_End":  "",
            "SearchSelector": "img.results_img",
            "Attribute": {},
            "tag": "div",
            "tag_class": "row",
            "ResultSelector": "div.indigo-recordinfo-image-link",
            "Result_URL_Start": "https://digitalna.nsk.hr",
            "Visible": True,
            "CAPTCHA": False
        }
    }
    

    #for libs in Library: print(Library[libs]["Name"])
    #for libs in Library: print(Library[libs]["Attribute"])

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
        '''for key, value in results.items():
            for v in value:
                print(key, v[0])'''

    return(results)


def Find_Bur_Results(Query, SpecifiedLibs: list[str] = None, NumResults: int = 2, max_workers: int = 9, timeout= 15000, toggle: bool = False):
    """
    Uses Search Feature on National Bureaus simultaneously using a given query.
    
    Args:
        Query (str): The search queried directly to bureaus.

        SpecifiedLibs (list[str]): Additional bureau sources to include in the search. 

        NumResults (int, optional): The number of top results scraped and outputted per bureau search. Default is 4.

        max_workers (int, optional): The maximum number of concurrent threads used. Defaults to 6.

        timeout (int): Maximum time (ms, 1000ms = 1sec) to wait for a page to load.

        toggle (bool): Toggle a specified only search with 4 more results without the always call bureaus.

    Returns:
        dict: A dictionary mapping each bureau name to a list of result links and visible text extracted. 

    Notes:
        - The function always calls a set of priority bureau ontop of those specified in the parameter.
        - If a bureau search fails or finds no result to scrape the dict entry defaults to [], and execution continues.
    """
    ToggleExtraSearches = 4
    
    libsToCheck = ["France","South Africa","United Kingdom","United States","Spain","Portugal","Germany","Netherlands","Belgium","China","Brazil","Mexico","Sweden","Canada","Phillipines"]
    ResultsPerLib = NumResults
    Search = Query

    # Merge List of libs to always search and specified libs 
    if (SpecifiedLibs != None):  libsToCheck = list(set(libsToCheck + SpecifiedLibs))

    if (toggle and (SpecifiedLibs != None)): 
        libsToCheck = SpecifiedLibs
        ResultsPerLib += ToggleExtraSearches

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
        },
        "South Africa":{
            "Name": "Statistics South Africa",
            "URL_Start": "https://www.statssa.gov.za/?s=",
            "URL_End": "&sitem=publications",
            "SearchSelector": "div.tab-pane",
            "Attribute": {"class": "btn"},
            "tag": "div",
            "tag_class": "tab-pane",
            "ResultSelector": "div.well",
            "Result_URL_Start": " ",
            "Visible": True,
            "CAPTCHA": False
        },
        "United Kingdom":{
            "Name": "UK Office for national statistics",
            "URL_Start": "https://www.ons.gov.uk/search?q=",
            "URL_End": "",
            "SearchSelector": "li.search__results__item",
            "Attribute": {"data-gtm-search-result-page": "1"},
            "tag": "li",
            "tag_class": "search__results__item",
            "ResultSelector": "div.section__content--markdown",
            "Result_URL_Start": "https://www.ons.gov.uk",
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
        "Spain":{ # Spain Needs Further Testing
            "Name": "Spanish National Institute of Statistics",
            "URL_Start": "https://www.ine.es/buscar/searchResults.do?searchString=",
            "URL_End": "&Menu_botonBuscador=&searchType=DEF_SEARCH&startat=0&L=1",
            "SearchSelector": "li.records",
            "Attribute": {"class": "rBuscFiles"},
            "tag": "li",
            "tag_class": "records",
            "ResultSelector": "span.title",
            "Result_URL_Start": "https://www.ine.es/",
            "Visible": True,
            "CAPTCHA": False
        },
        "Portugal":{ 
            "Name": "National Institute of Statistics Portugal",
            "URL_Start": "https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_pesquisa&frm_accao=PESQUISAR&frm_show_page_num=1&frm_modo_pesquisa=PESQUISA_SIMPLES&frm_texto=",
            "URL_End": "&frm_modo_texto=MODO_TEXTO_ALL&frm_data_ini=&frm_data_fim=&frm_tema=QUALQUER_TEMA&frm_area=o_ine_area_Publicacoes",
            "SearchSelector": "table.pesquisa_cells_coladas",
            "Attribute": {"class": "linkdestaques"},
            "tag": "div",
            "tag_class": "linkdestaques",
            "ResultSelector": "img.img-responsive",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Germany":{ 
            "Name": "Germany Federal Statistical Office",
            "URL_Start": "https://www.destatis.de/SiteGlobals/Forms/Suche/EN/Expertensuche_Formular.html?templateQueryString=",
            "URL_End": "&documentType_=publication#searchresults",
            "SearchSelector": "div.c-result__doctype",
            "Attribute": {},
            "tag": "h3",
            "tag_class": "c-result__heading",
            "ResultSelector": "strong.label",
            "Result_URL_Start": "https://www.destatis.de/",
            "Visible": True,
            "CAPTCHA": False
        },
        "Netherlands":{ 
            "Name": "Statistics Netherlands (CBS)",
            "URL_Start": "https://www.cbs.nl/en-gb/search?q=",
            "URL_End": "&selectedtypes=publications&selectedperiod=all-periods&startdate=&enddate=&sortorder=0",
            "SearchSelector": "h3.d-lg-block",
            "Attribute": {},
            "tag": "div",
            "tag_class": "col-lg-10",
            "ResultSelector": "img.img-fluid",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Belgium":{ 
            "Name": "Statbel the Belgian statistical office",
            "URL_Start": "https://statbel.fgov.be/en/search?search_api_fulltext_block=",
            "URL_End": "&items_per_page=10",
            "SearchSelector": "div.field",
            "Attribute": {"class":"more-link"},
            "tag": "div",
            "tag_class": "views-row",
            "ResultSelector": "h1.page-header",
            "Result_URL_Start": "https://statbel.fgov.be",
            "Visible": True,
            "CAPTCHA": False
        },
        "China":{ 
            "Name": "National Bureau of Statistics of China",
            "URL_Start": "https://www.stats.gov.cn/search/english/s?qt=",
            "URL_End": "",
            "SearchSelector": "div.content",
            "Attribute": {"class":"fontlan"},
            "tag": "div",
            "tag_class": "news",
            "ResultSelector": "div.cont",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Brazil":{
            "Name": "Brazilian Institute of Geography and Statistics",
            "URL_Start": "https://www.ibge.gov.br/en/busca.html?searchword=",
            "URL_End": "",
            "SearchSelector": "div.busca__item ",
            "Attribute": {"target":"_blank"},
            "tag": "p",
            "tag_class": "busca__item--link",
            "ResultSelector": "span.itens_conteudos",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Mexico":{
            "Name": "National System of Statistical and Geographical Information",
            "URL_Start": "https://en.www.inegi.org.mx/app/buscador/default.html?q=",
            "URL_End": "",
            "SearchSelector": "div.img-prod-map",
            "Attribute": {"id": re.compile(r"^TituloHip-\d+$")},
            "tag": "div",
            "tag_class": "col-xs-12",
            "ResultSelector": "img.bbl-sombreado",
            "Result_URL_Start": "https://en.www.inegi.org.mx",
            "Visible": True,
            "CAPTCHA": False
        },
        "Sweden":{
            "Name": "Statistics Sweden",
            "URL_Start": "https://www.scb.se/en/finding-statistics/search/?query=census&Category=Publications&Date=Anytime&Q=",
            "URL_End": "&Page=1",
            "SearchSelector": "h4.title",
            "Attribute": {},
            "tag": "li",
            "tag_class": "article",
            "ResultSelector": "div.row",
            "Result_URL_Start": "https://www.scb.se",
            "Visible": True,
            "CAPTCHA": False
        },
        "Canada":{
            "Name": "Statistics Canada",
            "URL_Start": "https://www.statcan.gc.ca/search/results/site-search?q=",
            "URL_End": "&op=&fq=stclac:2",
            "SearchSelector": "span.results_description",
            "Attribute": {"ng-click":"openurl(url);"},
            "tag": "li",
            "tag_class": "mrgn-bttm-md",
            "ResultSelector": "div.mrgn-tp-md",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        },
        "Phillipines":{
            "Name": "Republic of the Philippines Statistics Authority",
            "URL_Start": "https://psa.gov.ph/search/content?keys=",
            "URL_End": "",
            "SearchSelector": "div.content",
            "Attribute": {},
            "tag": "ol",
            "tag_class": None,
            "ResultSelector": "h3.page-title",
            "Result_URL_Start": "",
            "Visible": True,
            "CAPTCHA": False
        }
    }
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
        '''for key, value in results.items():
            for v in value:
                print(key, v[0])'''

    return(results)

