import requests
import time,os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from .Worker_library import scrape_library  # type: ignore

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from db.db import SessionLocal
from db.models import Library as LibraryModel, Bureau as BureauModel

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

    # Use the global database-backed Library object (defined at module level, line 120)
    # It automatically fetches data from the database when accessed via Library[country]
    # No need to define a local Library dict here

    # The following massive hardcoded dict has been removed to use the database instead:
    # Old code had 380+ lines of hardcoded library configurations
    # Now using: Library = DBBackedLibrary() from line 120

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

    # Use the global database-backed Bureau object (defined at module level, line 121)
    # Removed hardcoded Bureau dictionary - now using database
    # Note: The variable below should be "Bureau" not "Library" for bureau searches

    # OLD HARDCODED DICTIONARY REMOVED (was ~250 lines)
    # Now using global Bureau = DBBackedBureau() from line 121

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(scrape_library, Bureau, lib, Search, ResultsPerLib,timeout = timeout): lib
            for lib in libsToCheck
        }

        results = {}
        for future in as_completed(futures):
            lib_name = futures[future]
            try:
                results[lib_name] = future.result()
            except Exception as e:
                print(f"{lib_name} failed: {e}")

    return(results)
