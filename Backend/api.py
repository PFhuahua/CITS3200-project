from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from fastapi import Depends, Body
from db.db import SessionLocal
from db import models
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
from typing import List, Optional, Dict, Any
import asyncio
import json
import os
import tempfile
import zipfile
from datetime import datetime
import uuid
import time
import csv
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import existing scraping tools
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GoogleSearch_WS.ScraperTool import scrape_pdfs, process_pdf_link
from googlesearch import search as google_search
from GoogleSearch_WS.AITool import generate_all_queries, match_result, rank_web_results
from GoogleSearch_WS.Func_Library import Find_Lib_Results, Find_Bur_Results
from GoogleSearch_WS.Func_PDF_GoogleWS import PDF_Google_WS
# Note: LinkToDownload.py is interactive, we'll create a download function

app = FastAPI(
    title="Census PDF Finder API",
    description="API for searching and downloading census PDFs",
    version="1.0.0"
)
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # Your current frontend port
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
        "http://localhost:4173",  # Vite preview port
        "http://127.0.0.1:4173",
        "http://localhost:5174",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class SearchRequest(BaseModel):
    year: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    keyword: Optional[str] = None
    max_results: int = 20

class CensusDocument(BaseModel):
    id: str
    titleEnglish: str
    titleOriginal: Optional[str] = None
    country: str
    province: Optional[str] = None
    censusYear: int
    publicationYear: int
    authorPublisher: str
    fileSizeMB: float
    numberOfPages: int
    volumeNumber: Optional[str] = None
    fileTypes: List[str]
    url: str
    description: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[CensusDocument]
    total: int
    searchTime: float
    query: str

class DownloadRequest(BaseModel):
    document_ids: List[str]

# In-memory storage for search results (in production, use a database)
search_cache: Dict[str, List[CensusDocument]] = {}

def build_search_query(request: SearchRequest) -> str:
    """
    Construct a search query string from the user's search parameters.

    How it works:
    - The function accepts a SearchRequest object containing optional fields: keyword, country, state, year, and max_results.
    - It assembles non-empty or specific fields into a list in order of relevance.
    - If a field is present and not set to its generic "all-*" value, it's included.
        * For example, if country is not "all-countries", it is added.
        * Likewise for state and keyword.
    - For the year, if a specific year (not "all-years") is provided, it adds "census {year}".
        * Otherwise, it just adds the word "census".
    - All parts are joined by spaces into a single string which is used as the search query.

    Example:
        request = SearchRequest(keyword="population", country="Mexico", state="Chiapas", year="1930")
        build_search_query(request)
        # yields: "population Mexico Chiapas census 1930"
    """
    query_parts = []

    if request.keyword:
        query_parts.append(request.keyword)

    if request.country and request.country != "all-countries":
        query_parts.append(request.country)

    if request.state and request.state != "all-states":
        query_parts.append(request.state)

    if request.year and request.year != "all-years":
        query_parts.append(f"census {request.year}")
    else:
        query_parts.append("census")

    return " ".join(query_parts)

def convert_scraped_to_census_document(scraped_item: Dict[str, Any], request: SearchRequest, query: str) -> CensusDocument:
    """Convert scraped PDF data to CensusDocument format"""
    filename = scraped_item.get("filename", "Unknown Document")
    url = scraped_item.get("url", "")
    size = scraped_item.get("size", 0)

    # Extract year from filename or URL
    census_year = 2020  # Default
    if request.year and request.year != "all-years":
        census_year = int(request.year)

    # Extract country from query
    country = "Unknown"
    if request.country and request.country != "all-countries":
        country = request.country.replace("-", " ").title()

    return CensusDocument(
        id=str(uuid.uuid4()),
        titleEnglish=filename.replace(".pdf", "").replace("_", " ").title(),
        titleOriginal=None,
        country=country,
        province=request.state if request.state and request.state != "all-states" else None,
        censusYear=census_year,
        publicationYear=census_year + 1,
        authorPublisher="Census Bureau",
        fileSizeMB=round(size / (1024 * 1024), 2) if size else 0,
        numberOfPages=0,  # Would need to analyze PDF to get this
        volumeNumber=None,
        fileTypes=["PDF"],
        url=url,
        description=f"Census document found for query: {query}"
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/diagnostics")
async def diagnostics(db: Session = Depends(get_db)):
    """Diagnostic endpoint to check database status"""
    try:
        library_count = db.query(models.Library).count()
        bureau_count = db.query(models.Bureau).count()

        # Get sample countries
        lib_countries = db.query(models.Library.country).distinct().limit(5).all()
        bur_countries = db.query(models.Bureau.country).distinct().limit(5).all()

        # Check environment variables
        env_vars = {
            "GEMINI_API_KEY": bool(os.environ.get("GEMINI_API_KEY")),
            "SEARCH_ID": bool(os.environ.get("SEARCH_ID"))
        }

        return {
            "status": "ok",
            "database": {
                "libraries_count": library_count,
                "bureaus_count": bureau_count,
                "sample_library_countries": [c[0] for c in lib_countries],
                "sample_bureau_countries": [c[0] for c in bur_countries]
            },
            "environment": env_vars
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Libraries
class LibraryBase(BaseModel):
    name: str = Field(..., alias="Name")
    url_start: str = Field(..., alias="URL_Start")
    country: str = Field(..., alias="Country")

    url_end: str | None = Field("", alias="URL_End")
    result_url_start: str | None = Field("", alias="Result_URL_Start")
    search_selector: str | None = Field("", alias="SearchSelector")
    attribute: dict | None = Field({}, alias="Attribute")
    tag: str = Field("", alias="tag")
    tag_class: str = Field("", alias="tag_class")
    result_selector: str = Field("", alias="ResultSelector")
    visible: bool = Field(True, alias="Visible")
    priority: int = Field(1, alias="Priority")
    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        extra = "ignore"
class LibraryCreate(LibraryBase):
    pass

class LibraryUpdate(BaseModel):
    name: str | None = Field(None, alias="Name")
    url_start: str | None = Field(None, alias="URL_Start")
    url_end: str | None = Field(None, alias="URL_End")
    result_url_start: str | None = Field(None, alias="Result_URL_Start")
    search_selector: str | None = Field(None, alias="SearchSelector")
    attribute: dict | None = Field(None, alias="Attribute")
    tag: str | None = Field(None, alias="tag")
    tag_class: str | None = Field(None, alias="tag_class")
    result_selector: str | None = Field(None, alias="ResultSelector")
    visible: bool | None = Field(None, alias="Visible")
    priority: int | None = Field(None, alias="Priority")
    country: str | None = Field(None, alias="Country")
    captcha: bool | None = Field(None, alias="CAPTCHA")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        extra = "ignore"


@app.post("/api/libraries/")
def create_library(library_data: dict, db: Session = Depends(get_db)):
    def normalize_keys(d: dict):
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = normalize_keys(v)
            new_dict[k.lower()] = v
        return new_dict
    library_data = normalize_keys(library_data)
    
    if len(library_data) == 1:
        country, info = list(library_data.items())[0]
        info["Country"] = country
        info.setdefault("Name", country) 
    else:
        info = library_data

    info.pop("CAPTCHA", None)

    defaults = {
        "URL_End": "",
        "Result_URL_Start": "",
        "SearchSelector": "",
        "Attribute": {},
        "tag": "",
        "tag_class": "",
        "ResultSelector": "",
        "Visible": True,
        "Priority": 1,
    }
    for key, value in defaults.items():
        info.setdefault(key, value)
    
    lib = LibraryCreate(**info)
    db_lib = models.Library(**lib.dict())
    db.add(db_lib)
    db.commit()
    db.refresh(db_lib)
    return db_lib

@app.get("/api/libraries/")
def list_libraries(db: Session = Depends(get_db)):
    return db.query(models.Library).order_by(models.Library.priority.desc()).all()

@app.put("/api/libraries/{lib_id}")
def update_library(lib_id: int, library: LibraryUpdate, db: Session = Depends(get_db)):
    db_lib = db.query(models.Library).filter(models.Library.id == lib_id).first()
    if not db_lib:
        raise HTTPException(status_code=404, detail="Library not found")
    for key, value in library.dict(exclude_unset=True).items():
        setattr(db_lib, key, value)
    db.commit()
    db.refresh(db_lib)
    return db_lib

@app.delete("/api/libraries/{lib_id}")
def delete_library(lib_id: int, db: Session = Depends(get_db)):
    db_lib = db.query(models.Library).filter(models.Library.id == lib_id).first()
    if not db_lib:
        raise HTTPException(status_code=404, detail="Library not found")
    db.delete(db_lib)
    db.commit()
    return {"message": f"Library {lib_id} deleted successfully"}

@app.post("/api/import-libraries")
def import_libraries():
    ## Import all libraries from backend/data/libraries.json into the database.
    db = SessionLocal()

    try:
        with open("Backend/data/libraries.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for country, info in data.items():

            lib = models.Library(
                name=info["Name"],
                url_start=info["URL_Start"],
                result_url_start=info.get("Result_URL_Start", ""),
                url_end=info.get("URL_End", ""),
                search_selector=info["SearchSelector"],
                attribute=info["Attribute"],
                tag=info.get("tag", ""),
                tag_class=info.get("tag_class", ""),
                result_selector=info.get("ResultSelector", ""),
                visible=info.get("Visible", True),
                priority=info.get("Priority", 1),
                country=country,
                captcha=info.get("CAPTCHA", False)
            )
            db.add(lib)

        db.commit()
        return {"message": "Libraries imported success"}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="libraries.json not found")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    finally:
        db.close()
class BureauBase(BaseModel):
    name: str = Field(..., alias="Name")
    url_start: str = Field(..., alias="URL_Start")
    country: str = Field(..., alias="Country")

    url_end: str | None = Field("", alias="URL_End")
    result_url_start: str | None = Field("", alias="Result_URL_Start")
    search_selector: str | None = Field("", alias="SearchSelector")
    attribute: dict | None = Field({}, alias="Attribute")
    tag: str = Field("", alias="tag")
    tag_class: str = Field("", alias="tag_class")
    result_selector: str = Field("", alias="ResultSelector")
    visible: bool = Field(True, alias="Visible")
    priority: int = Field(1, alias="Priority")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        extra = "ignore"

class BureauCreate(BureauBase):
    pass

class BureauUpdate(BaseModel):
    name: str | None = Field(None, alias="Name")
    url_start: str | None = Field(None, alias="URL_Start")
    url_end: str | None = Field(None, alias="URL_End")
    result_url_start: str | None = Field(None, alias="Result_URL_Start")
    search_selector: str | None = Field(None, alias="SearchSelector")
    attribute: dict | None = Field(None, alias="Attribute")
    tag: str | None = Field(None, alias="tag")
    tag_class: str | None = Field(None, alias="tag_class")
    result_selector: str | None = Field(None, alias="ResultSelector")
    visible: bool | None = Field(None, alias="Visible")
    priority: int | None = Field(None, alias="Priority")
    country: str | None = Field(None, alias="Country")
    captcha: bool | None = Field(None, alias="CAPTCHA")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
        extra = "ignore"

@app.post("/api/bureaus/")
def create_bureau(bureau_data: dict, db: Session = Depends(get_db)):
    def normalize_keys(d: dict):
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = normalize_keys(v)
            new_dict[k.lower()] = v
        return new_dict

    bureau_data = normalize_keys(bureau_data)

    if len(bureau_data) == 1:
        country, info = list(bureau_data.items())[0]
        info["country"] = country
        info.setdefault("name", country) 
    else:
        info = bureau_data

    info.pop("captcha", None)

    defaults = {
        "url_end": "",
        "result_url_start": "",
        "searchselector": "",
        "attribute": {},
        "tag": "",
        "tag_class": "",
        "resultselector": "",
        "visible": True,
        "priority": 1,
    }
    for key, value in defaults.items():
        info.setdefault(key, value)

    bur = BureauCreate(**info)
    db_bureau = models.Bureau(**bur.dict())
    db.add(db_bureau)
    db.commit()
    db.refresh(db_bureau)
    return db_bureau

@app.get("/api/bureaus/")
def list_bureaus(db: Session = Depends(get_db)):
    return db.query(models.Bureau).order_by(models.Bureau.priority.desc()).all()

@app.put("/api/bureaus/{bureau_id}")
def update_bureau(bureau_id: int, bureau: BureauUpdate, db: Session = Depends(get_db)):
    db_bureau = db.query(models.Bureau).filter(models.Bureau.id == bureau_id).first()
    if not db_bureau:
        raise HTTPException(status_code=404, detail="Bureau not found")
    for key, value in bureau.dict(exclude_unset=True).items():
        setattr(db_bureau, key, value)
    db.commit()
    db.refresh(db_bureau)
    return db_bureau

@app.delete("/api/bureaus/{bureau_id}")
def delete_bureau(bureau_id: int, db: Session = Depends(get_db)):
    db_bureau = db.query(models.Bureau).filter(models.Bureau.id == bureau_id).first()
    if not db_bureau:
        raise HTTPException(status_code=404, detail="Bureau not found")
    db.delete(db_bureau)
    db.commit()
    return {"message": f"Bureau {bureau_id} deleted successfully"}

@app.post("/api/import-bureaus")
def import_bureaus():
    ##Import all bureaus from backend/data/bureaus.json into the database.
    db = SessionLocal()
    try:
        with open("Backend/data/bureaus.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for country, info in data.items():
            bureau = models.Bureau(
                name=info["Name"],
                url_start=info["URL_Start"],
                result_url_start=info.get("Result_URL_Start", ""),
                url_end=info.get("URL_End", ""),
                search_selector=info["SearchSelector"],
                attribute=info["Attribute"],
                tag=info.get("tag", ""),
                tag_class=info.get("tag_class", ""),
                result_selector=info.get("ResultSelector", ""),
                visible=info.get("Visible", True),
                priority=info.get("Priority", 1),
                country=country,
                captcha=info.get("CAPTCHA", False)
            )
            db.add(bureau)

        db.commit()
        return {"message": "Bureaus imported success"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="bureaus.json not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
    finally:
        db.close()

# FilterLinks
class FilterLinkCreate(BaseModel):
    link: str

class FilterLinkUpdate(BaseModel):
    link: str | None = None

@app.post("/api/filters/")
def create_filter(filter_link: FilterLinkCreate, db: Session = Depends(get_db)):
    db_filter = models.FilterLink(**filter_link.dict())
    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)
    return db_filter

@app.get("/api/filters/")
def list_filters(db: Session = Depends(get_db)):
    return db.query(models.FilterLink).all()

@app.put("/api/filters/{filter_id}")
def update_filter(filter_id: int, filter_link: FilterLinkUpdate, db: Session = Depends(get_db)):
    db_filter = db.query(models.FilterLink).filter(models.FilterLink.id == filter_id).first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    for key, value in filter_link.dict(exclude_unset=True).items():
        setattr(db_filter, key, value)
    db.commit()
    db.refresh(db_filter)
    return db_filter

@app.delete("/api/filters/{filter_id}")
def delete_filter(filter_id: int, db: Session = Depends(get_db)):
    db_filter = db.query(models.FilterLink).filter(models.FilterLink.id == filter_id).first()
    if not db_filter:
        raise HTTPException(status_code=404, detail="Filter not found")
    db.delete(db_filter)
    db.commit()
    return {"message": f"Filter {filter_id} deleted successfully"}

# Cascading Search Flow Models
class CascadingSearchRequest(BaseModel):
    english_title: str = Field(..., alias="englishTitle")
    original_title: str | None = Field(None, alias="originalTitle")
    country: str
    province: str | None = None
    cite: str | None = None
    publisher: str | None = None
    volume: str | None = None
    coloniser: str | None = None
    num_lib_results: int = Field(2, alias="numLibResults")
    num_bur_results: int = Field(5, alias="numBurResults")
    ws_results: int = Field(5, alias="wsResults")
    ws_amt: int = Field(15, alias="wsAmt")
    max_workers: int = Field(9, alias="maxWorkers")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

class CascadingSearchResponse(BaseModel):
    phase: str  # "library", "bureau", or "web"
    queries: List[str]
    results: List[Any]
    time_taken: float
    status: str  # "success" or "no_results"

class BatchSearchItem(BaseModel):
    row_number: int
    english_title: str
    country: str
    original_title: Optional[str] = None
    province: Optional[str] = None
    cite: Optional[str] = None
    publisher: Optional[str] = None
    volume: Optional[str] = None
    coloniser: Optional[str] = None

class BatchSearchResult(BaseModel):
    row_number: int
    search_input: BatchSearchItem
    search_result: Optional[CascadingSearchResponse] = None
    error: Optional[str] = None

class BatchSearchResponse(BaseModel):
    total_rows: int
    successful_searches: int
    failed_searches: int
    results: List[BatchSearchResult]
    total_time_taken: float

@app.post("/api/cascading-search", response_model=CascadingSearchResponse)
async def cascading_search(request: CascadingSearchRequest):
    """
    Performs cascading search: Libraries -> Bureaus -> Web
    Stops at first successful phase
    """
    try:
        # Check for required API keys
        if not os.environ.get("GEMINI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY not configured. Please set the environment variable."
            )

        start_time = time.time()

        # Build input dictionary for query generation
        input_dict = {
            "English Title": request.english_title,
            "Original Title": request.original_title or "N/A",
            "Country": request.country,
            "Province": request.province or "N/A",
            "Cite": request.cite or "N/A",
            "Publisher": request.publisher or "N/A",
            "Volume": request.volume or "N/A",
            "Coloniser": request.coloniser or "N/A"
        }

        # Query generation phase
        doc_info = ", ".join(f"{key}: {value}" for key, value in input_dict.items())
        try:
            queries_json = generate_all_queries(doc_info)
            all_queries = json.loads(queries_json)

            # Validate that we have the expected structure: [[lib_queries], [bur_queries], [web_queries]]
            if not all_queries or not isinstance(all_queries, list):
                raise HTTPException(status_code=400, detail="Invalid query format returned")

            if len(all_queries) < 3:
                raise HTTPException(
                    status_code=400,
                    detail=f"Expected 3 query sets (library, bureau, web), got {len(all_queries)}. Queries: {all_queries}"
                )

            # Validate each query set is a list
            for i, query_set in enumerate(all_queries[:3]):
                if not isinstance(query_set, list):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Query set {i} is not a list: {query_set}"
                    )
                if not query_set or all(q.strip() == "" for q in query_set):
                    print(f"Warning: Query set {i} is empty or contains only empty strings")

            # Log all generated queries
            print(f"[QUERY GENERATION] Library queries: {all_queries[0]}")
            print(f"[QUERY GENERATION] Bureau queries: {all_queries[1]}")
            print(f"[QUERY GENERATION] Web queries: {all_queries[2]}")

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating queries: {str(e)}")

        # Phase 1: Library search
        lib_queries = all_queries[0]
        print(f"[LIBRARY PHASE] Starting with queries: {lib_queries}")
        lib_all_results = []
        for query in lib_queries:
            try:
                print(f"[LIBRARY PHASE] Searching with query: {query.strip()}")
                lib_response = Find_Lib_Results(
                    query.strip(),
                    [request.country,request.coloniser],
                    request.num_lib_results,
                    request.max_workers
                )
                print(f"[LIBRARY PHASE] Response keys: {lib_response.keys()}")
                print(f"[LIBRARY PHASE] Response sample: {dict(list(lib_response.items())[:2])}")

                if not all(v == "" or v == [] for v in lib_response.values()):
                    lib_all_results.append(lib_response)
                    print(f"[LIBRARY PHASE] Added results to lib_all_results")
                else:
                    print(f"[LIBRARY PHASE] No valid results found for this query")
            except Exception as e:
                print(f"[LIBRARY PHASE] Library search error: {e}")
                import traceback
                traceback.print_exc()
                continue

        print(f"[LIBRARY PHASE] Total results collected: {len(lib_all_results)}")
        if lib_all_results:
            try:
                match_res = match_result(lib_queries, lib_all_results)
                lib_result = json.loads(match_res)
                if lib_result and lib_result != []:
                    lib_time = time.time() - start_time
                    return CascadingSearchResponse(
                        phase="library",
                        queries=lib_queries,
                        results=lib_result,
                        time_taken=lib_time,
                        status="success"
                    )
            except Exception as e:
                print(f"Error matching library results: {e}")

        # Phase 2: Bureau search
        lib_time = time.time()
        bur_queries = all_queries[1]
        print(f"[BUREAU PHASE] Starting with queries: {bur_queries}")
        bur_all_results = []
        for query in bur_queries:
            try:
                print(f"[BUREAU PHASE] Searching with query: {query.strip()}")
                bur_response = Find_Bur_Results(
                    query.strip(),
                    [request.country,request.coloniser],
                    request.num_bur_results,
                    request.max_workers
                )
                print(f"[BUREAU PHASE] Response keys: {bur_response.keys()}")
                print(f"[BUREAU PHASE] Response sample: {dict(list(bur_response.items())[:2])}")

                if not all(v == "" or v == [] for v in bur_response.values()):
                    bur_all_results.append(bur_response)
                    print(f"[BUREAU PHASE] Added results to bur_all_results")
                else:
                    print(f"[BUREAU PHASE] No valid results found for this query")
            except Exception as e:
                print(f"[BUREAU PHASE] Bureau search error: {e}")
                import traceback
                traceback.print_exc()
                continue

        print(f"[BUREAU PHASE] Total results collected: {len(bur_all_results)}")
        if bur_all_results:
            try:
                match_res = match_result(bur_queries, bur_all_results)
                bur_result = json.loads(match_res)
                if bur_result and bur_result != []:
                    bur_time = time.time() - lib_time
                    return CascadingSearchResponse(
                        phase="bureau",
                        queries=bur_queries,
                        results=bur_result,
                        time_taken=bur_time,
                        status="success"
                    )
            except Exception as e:
                print(f"Error matching bureau results: {e}")

        # Phase 3: Web search
        bur_time = time.time()
        web_queries = all_queries[2]
        print(f"[WEB PHASE] Starting with queries: {web_queries}")
        web_all_results = []

        # Get API keys from environment
        google_api_key = os.environ.get("GEMINI_API_KEY")
        search_cx = os.environ.get("SEARCH_ID")

        if not google_api_key or not search_cx:
            print("[WEB PHASE] Warning: GEMINI_API_KEY or SEARCH_ID not found in environment")
            print(f"[WEB PHASE] GEMINI_API_KEY present: {bool(google_api_key)}")
            print(f"[WEB PHASE] SEARCH_ID present: {bool(search_cx)}")

        for query in web_queries:
            try:
                print(f"[WEB PHASE] Searching with query: {query.strip()}")
                web_response = PDF_Google_WS(
                    query.strip(),
                    MaxPDFs=request.ws_results,
                    ResultsSearched=request.ws_amt,
                    api_key=google_api_key,
                    Searchcx=search_cx
                )
                print(f"[WEB PHASE] Response length: {len(web_response) if web_response else 0}")
                if web_response:
                    web_all_results.append(web_response)
                    print(f"[WEB PHASE] Added {len(web_response)} results")
                else:
                    print(f"[WEB PHASE] No results from this query")
            except Exception as e:
                print(f"[WEB PHASE] Web search error: {e}")
                import traceback
                traceback.print_exc()
                continue

        print(f"[WEB PHASE] Total results collected: {len(web_all_results)}")
        if web_all_results:
            try:
                rank_res = rank_web_results(web_queries[0], web_all_results)
                web_result = json.loads(rank_res)
                if web_result and web_result != []:
                    web_time = time.time() - bur_time
                    return CascadingSearchResponse(
                        phase="web",
                        queries=web_queries,
                        results=web_result[:3],  # Top 3 results
                        time_taken=web_time,
                        status="success"
                    )
            except Exception as e:
                print(f"Error ranking web results: {e}")

        # No results found in any phase
        total_time = time.time() - start_time
        return CascadingSearchResponse(
            phase="none",
            queries=web_queries if web_queries else [],
            results=[],
            time_taken=total_time,
            status="no_results"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cascading search failed: {str(e)}")

def perform_single_cascading_search(search_item: BatchSearchItem) -> tuple[int, Optional[CascadingSearchResponse], Optional[str]]:
    """
    Helper function to perform a single cascading search.
    Returns (row_number, result, error)
    """
    try:
        # Build CascadingSearchRequest
        request = CascadingSearchRequest(
            englishTitle=search_item.english_title,
            originalTitle=search_item.original_title,
            country=search_item.country,
            province=search_item.province,
            cite=search_item.cite,
            publisher=search_item.publisher,
            volume=search_item.volume,
            coloniser=search_item.coloniser,
            numLibResults=2,
            numBurResults=5,
            wsResults=5,
            wsAmt=15,
            maxWorkers=9
        )

        start_time = time.time()

        # Build input dictionary for query generation
        input_dict = {
            "English Title": request.english_title,
            "Original Title": request.original_title or "N/A",
            "Country": request.country,
            "Province": request.province or "N/A",
            "Cite": request.cite or "N/A",
            "Publisher": request.publisher or "N/A",
            "Volume": request.volume or "N/A",
            "Coloniser": request.coloniser or "N/A"
        }

        # Query generation phase
        doc_info = ", ".join(f"{key}: {value}" for key, value in input_dict.items())
        queries_json = generate_all_queries(doc_info)
        all_queries = json.loads(queries_json)

        if not all_queries or not isinstance(all_queries, list) or len(all_queries) < 3:
            return (search_item.row_number, None, "Invalid query format returned from AI")

        # Phase 1: Library search
        lib_queries = all_queries[0]
        lib_all_results = []
        for query in lib_queries:
            try:
                lib_response = Find_Lib_Results(
                    query.strip(),
                    [request.country,request.coloniser],
                    request.num_lib_results,
                    request.max_workers
                )
                if not all(v == "" or v == [] for v in lib_response.values()):
                    lib_all_results.append(lib_response)
            except Exception as e:
                print(f"Library search error for row {search_item.row_number}: {e}")
                continue

        if lib_all_results:
            try:
                match_res = match_result(doc_info, lib_all_results)
                lib_result = json.loads(match_res)
                if lib_result and lib_result != []:
                    lib_time = time.time() - start_time
                    return (search_item.row_number, CascadingSearchResponse(
                        phase="library",
                        queries=lib_queries,
                        results=lib_result,
                        time_taken=lib_time,
                        status="success"
                    ), None)
            except Exception as e:
                print(f"Error matching library results for row {search_item.row_number}: {e}")

        # Phase 2: Bureau search
        lib_time = time.time()
        bur_queries = all_queries[1]
        bur_all_results = []
        for query in bur_queries:
            try:
                bur_response = Find_Bur_Results(
                    query.strip(),
                    [request.country,request.coloniser],
                    request.num_bur_results,
                    request.max_workers
                )
                if not all(v == "" or v == [] for v in bur_response.values()):
                    bur_all_results.append(bur_response)
            except Exception as e:
                print(f"Bureau search error for row {search_item.row_number}: {e}")
                continue

        if bur_all_results:
            try:
                match_res = match_result(doc_info, bur_all_results)
                bur_result = json.loads(match_res)
                if bur_result and bur_result != []:
                    bur_time = time.time() - lib_time
                    return (search_item.row_number, CascadingSearchResponse(
                        phase="bureau",
                        queries=bur_queries,
                        results=bur_result,
                        time_taken=bur_time,
                        status="success"
                    ), None)
            except Exception as e:
                print(f"Error matching bureau results for row {search_item.row_number}: {e}")

        # Phase 3: Web search
        bur_time = time.time()
        web_queries = all_queries[2]
        web_all_results = []

        google_api_key = os.environ.get("GEMINI_API_KEY")
        search_cx = os.environ.get("SEARCH_ID")

        for query in web_queries:
            try:
                web_response = PDF_Google_WS(
                    query.strip(),
                    MaxPDFs=request.ws_results,
                    ResultsSearched=request.ws_amt,
                    api_key=google_api_key,
                    Searchcx=search_cx
                )
                if web_response:
                    web_all_results.append(web_response)
            except Exception as e:
                print(f"Web search error for row {search_item.row_number}: {e}")
                continue

        if web_all_results:
            try:
                rank_res = rank_web_results(web_queries[0], web_all_results)
                web_result = json.loads(rank_res)
                if web_result and web_result != []:
                    web_time = time.time() - bur_time
                    return (search_item.row_number, CascadingSearchResponse(
                        phase="web",
                        queries=web_queries,
                        results=web_result[:3],
                        time_taken=web_time,
                        status="success"
                    ), None)
            except Exception as e:
                print(f"Error ranking web results for row {search_item.row_number}: {e}")

        # No results found
        total_time = time.time() - start_time
        return (search_item.row_number, CascadingSearchResponse(
            phase="none",
            queries=web_queries if web_queries else [],
            results=[],
            time_taken=total_time,
            status="no_results"
        ), None)

    except Exception as e:
        return (search_item.row_number, None, str(e))

@app.post("/api/batch-search", response_model=BatchSearchResponse)
async def batch_cascading_search(file: UploadFile = File(...)):
    """
    Performs cascading search on multiple rows from a CSV file.
    CSV should have columns: Title (In English), Country, and optionally:
    Original title, Province, Date/Year of census, Author/Publisher, Volume number, Colonising power
    """
    try:
        # Check for required API keys
        if not os.environ.get("GEMINI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY not configured. Please set the environment variable."
            )

        # Read CSV file
        contents = await file.read()
        csv_text = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))

        # Parse CSV rows into BatchSearchItem objects
        search_items = []
        for idx, row in enumerate(csv_reader, start=1):
            # Skip header row if it exists (first row with "Table Name:")
            if idx == 1 and row.get('Table Name:', '') == 'Table Name:':
                continue

            # Extract fields from CSV
            english_title = row.get('Title (In English)', '').strip()
            country = row.get('Country', '').strip()

            # Skip rows without required fields
            if not english_title or not country:
                print(f"Skipping row {idx}: missing required fields (Title or Country)")
                continue

            search_item = BatchSearchItem(
                row_number=idx,
                english_title=english_title,
                country=country,
                original_title=row.get('Original title', '').strip() or None,
                province=row.get('Province', '').strip() or None,
                cite=row.get('Date/Year of census', '').strip() or None,
                publisher=row.get('Author/Publisher', '').strip() or None,
                volume=row.get('Volume number (if applicable)', '').strip() or None,
                coloniser=row.get('Colonising power', '').strip() or None
            )
            search_items.append(search_item)

        if not search_items:
            raise HTTPException(status_code=400, detail="No valid rows found in CSV file")

        print(f"[BATCH SEARCH] Processing {len(search_items)} items")

        # Perform searches in parallel with ThreadPoolExecutor
        start_time = time.time()
        results = []
        successful = 0
        failed = 0

        # Use ThreadPoolExecutor for parallel processing
        max_workers = min(3, len(search_items))  # Limit to 3 concurrent searches
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(perform_single_cascading_search, item): item
                for item in search_items
            }

            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    row_number, search_result, error = future.result()

                    if error:
                        failed += 1
                        results.append(BatchSearchResult(
                            row_number=row_number,
                            search_input=item,
                            search_result=None,
                            error=error
                        ))
                    else:
                        successful += 1
                        results.append(BatchSearchResult(
                            row_number=row_number,
                            search_input=item,
                            search_result=search_result,
                            error=None
                        ))

                    print(f"[BATCH SEARCH] Completed row {row_number}/{len(search_items)}")

                except Exception as e:
                    failed += 1
                    results.append(BatchSearchResult(
                        row_number=item.row_number,
                        search_input=item,
                        search_result=None,
                        error=str(e)
                    ))
                    print(f"[BATCH SEARCH] Error processing row {item.row_number}: {e}")

        # Sort results by row number
        results.sort(key=lambda x: x.row_number)
        print(["Search queries generated: "+str(x.search_input) for x in results])

        total_time = time.time() - start_time

        print(f"[BATCH SEARCH] Completed: {successful} successful, {failed} failed, {total_time:.2f}s total")

        return BatchSearchResponse(
            total_rows=len(search_items),
            successful_searches=successful,
            failed_searches=failed,
            results=results,
            total_time_taken=total_time
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch search failed: {str(e)}")

@app.post("/api/search", response_model=SearchResponse)
async def search_census_documents(request: SearchRequest):
    """Search for census documents using existing scraping tools"""
    start_time = datetime.now()

    try:
        # Build search query
        query = build_search_query(request)

        # Check cache first
        cache_key = f"{query}_{request.max_results}"
        if cache_key in search_cache:
            cached_results = search_cache[cache_key]
            return SearchResponse(
                results=cached_results,
                total=len(cached_results),
                searchTime=(datetime.now() - start_time).total_seconds(),
                query=query
            )

        # Use existing Google search functionality
        results = []

        # Use the imported google_search function

        # Set up search parameters based on existing testCensusWS.py
        ExactTags = []
        NonExactTags = []

        if request.keyword:
            NonExactTags.append(request.keyword)
        if request.country and request.country != "all-countries":
            NonExactTags.append(request.country)
        if request.state and request.state != "all-states":
            NonExactTags.append(request.state)

        NonExactTags.extend(["census", "data"])

        Filters = ["wikipedia"]  # Exclude Wikipedia
        MaxPDFs = request.max_results
        ResultsSearched = min(request.max_results * 2, 20)  # Search more results than needed

        # Execute search using existing logic from testCensusWS.py
        search_results = []

        try:
            # Build search query like in testCensusWS.py
            if ExactTags != []:
                exact_tags_str = ' '.join(f'"{tag}"' for tag in ExactTags)
            else:
                exact_tags_str = " "

            if NonExactTags != []:
                non_exact_tags_str = ' '.join(NonExactTags)
            else:
                non_exact_tags_str = " "

            Query = exact_tags_str + " " + non_exact_tags_str

            # Search using Google search like in testCensusWS.py
            FULL_RESULTS = []
            pdf_results = []

            for link in google_search(Query, num=ResultsSearched):
                if not any(f in link for f in Filters):
                    if ".pdf" in link.lower():
                        # Process PDF link directly
                        pdf_info = process_pdf_link(link)
                        FULL_RESULTS.append(pdf_info)
                        pdf_results.append((pdf_info["url"], pdf_info["size"]))
                    else:
                        # Non-PDF link -> scrape for PDFs
                        scraped = scrape_pdfs(link)
                        if scraped is None:
                            continue
                        for item in scraped:
                            FULL_RESULTS.append(item)
                            pdf_results.append((item["url"], item["size"]))
                            if len(pdf_results) > MaxPDFs:
                                break
                if len(pdf_results) > MaxPDFs:
                    break

            # Remove duplicates
            unique_results = list(set(pdf_results))

            # Convert to CensusDocument format
            for url, size in unique_results[:request.max_results]:
                # Find the full result data for this URL
                full_result = next((r for r in FULL_RESULTS if r["url"] == url), {})

                result_data = {
                    "url": url,
                    "filename": full_result.get("filename", f"document_{len(results)+1}.pdf"),
                    "size": size
                }

                census_doc = convert_scraped_to_census_document(result_data, request, query)
                results.append(census_doc)

        except Exception as e:
            print(f"Search error: {e}")
            # Return empty results on error
            pass

        # Cache results
        search_cache[cache_key] = results

        search_time = (datetime.now() - start_time).total_seconds()

        return SearchResponse(
            results=results,
            total=len(results),
            searchTime=search_time,
            query=query
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/download/{document_id}")
async def download_document(document_id: str):
    """Download a single document"""
    try:
        # Find document in cache
        document = None
        for cached_results in search_cache.values():
            for doc in cached_results:
                if doc.id == document_id:
                    document = doc
                    break
            if document:
                break

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Use existing download functionality
        # For now, return the URL for the document
        # In practice, you'd implement actual file downloading

        return {
            "download_url": document.url,
            "filename": document.titleEnglish + ".pdf",
            "size_mb": document.fileSizeMB
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/api/download/bulk")
async def download_bulk_documents(request: DownloadRequest):
    """Download multiple documents as ZIP"""
    try:
        documents = []

        # Find all requested documents
        for doc_id in request.document_ids:
            for cached_results in search_cache.values():
                for doc in cached_results:
                    if doc.id == doc_id:
                        documents.append(doc)
                        break
                if any(d.id == doc_id for d in documents):
                    break

        if not documents:
            raise HTTPException(status_code=404, detail="No documents found")

        # Create a temporary ZIP file
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
            with zipfile.ZipFile(tmp_file.name, 'w') as zip_file:
                for doc in documents:
                    # Add document info to ZIP
                    zip_file.writestr(
                        f"{doc.titleEnglish}.txt",
                        f"Title: {doc.titleEnglish}\n"
                        f"Country: {doc.country}\n"
                        f"Year: {doc.censusYear}\n"
                        f"URL: {doc.url}\n"
                        f"Size: {doc.fileSizeMB} MB"
                    )

        # Return the ZIP file
        return FileResponse(
            tmp_file.name,
            media_type='application/zip',
            filename=f"census_documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk download failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
