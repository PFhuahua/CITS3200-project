from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import os
import tempfile
import zipfile
from datetime import datetime
import uuid

# Import existing scraping tools
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GoogleSearch_WS.ScraperTool import scrape_pdfs, process_pdf_link
from googlesearch import search as google_search
# Note: LinkToDownload.py is interactive, we'll create a download function

app = FastAPI(
    title="Census PDF Finder API",
    description="API for searching and downloading census PDFs",
    version="1.0.0"
)

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
        "http://127.0.0.1:4173"
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
    """Build search query from request parameters"""
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
