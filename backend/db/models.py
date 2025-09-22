from sqlalchemy import (
    Column, String, Integer, Date, DateTime, Text,
    ForeignKey, JSON, Float
)
from sqlalchemy.orm import relationship
from backend.db.db import Base
import datetime

#Sources
class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False)          
    type = Column(String(50), nullable=False)         
    homepage_url = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    documents = relationship("Document", back_populates="source")


# Documents
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    external_id = Column(String(191))                   
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    published_at = Column(Date)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
    content_hash = Column(String(64))                   
    raw_metadata = Column(JSON)
    lang = Column(String(8))                            
    country_iso3 = Column(String(3))
    region_code = Column(String(50))                    
    topic = Column(String(100))                         
    status = Column(String(50), default="active")       
    source = relationship("Source", back_populates="documents")


# Searches
class Search(Base):
    __tablename__ = "searches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(Text, nullable=False)
    params = Column(JSON)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)
    status = Column(String(50), default="queued")      
    results = relationship("SearchResult", back_populates="search")


# Search Results
class SearchResult(Base):
    __tablename__ = "search_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, ForeignKey("searches.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    rank = Column(Integer)
    score = Column(Float)
    dedup_group_id = Column(Integer)

    search = relationship("Search", back_populates="results")
    document = relationship("Document")

# Batches
class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False)         
    created_by = Column(String(100))                
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="created")     
    summary = Column(JSON)

    queries = relationship("BatchQuery", back_populates="batch")


# Batch Queries
class BatchQuery(Base):
    __tablename__ = "batch_queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    query = Column(Text, nullable=False)
    status = Column(String(50), default="queued")
    result_count = Column(Integer, default=0)
    error_msg = Column(Text)

    batch = relationship("Batch", back_populates="queries")


# Countries
class Country(Base):
    __tablename__ = "countries"
    iso2 = Column(String(2), primary_key=True)
    iso3 = Column(String(3), unique=True, nullable=False)
    m49 = Column(Integer, unique=True)
    name_en = Column(String(191), nullable=False)       
    name_local = Column(String(191))   


# Regions
class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_iso3 = Column(String(3), ForeignKey("countries.iso3"))
    code = Column(String(50), nullable=False)           
    name = Column(String(191), nullable=False)   


# Audits
class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)    
    action = Column(String(50), nullable=False)         
    before = Column(JSON)
    after = Column(JSON)
    actor = Column(String(100))                         
    at = Column(DateTime, default=datetime.datetime.utcnow)
class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False)     
    url_start = Column(String(500), nullable=False)   
    url_end = Column(String(500))                       
    search_selector = Column(String(200), nullable=False)
    attribute = Column(JSON)                        
    tag = Column(String(50))
    tag_class = Column(String(100))
    result_selector = Column(String(200))
    visible = Column(Boolean, default=True)
    priority = Column(Integer, default=1)
    country = Column(String(100))
    captcha = Column(Boolean, default=False)   

class FilterLink(Base):
    __tablename__ = "filter_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(500), nullable=False) 