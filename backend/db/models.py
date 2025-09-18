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
    name = Column(String(191), nullable=False)          # 加长度
    type = Column(String(50), nullable=False)           # gov_site/lib/api
    homepage_url = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    documents = relationship("Document", back_populates="source")


# Documents
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    external_id = Column(String(191))                   # 给长度
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    published_at = Column(Date)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
    content_hash = Column(String(64))                   # 已有长度
    raw_metadata = Column(JSON)
    lang = Column(String(8))                            # 原来 (2)，稍微放宽
    country_iso3 = Column(String(3))
    region_code = Column(String(50))                    # 原来无长度
    topic = Column(String(100))                         # 原来无长度
    status = Column(String(50), default="active")       # 原来无长度

    source = relationship("Source", back_populates="documents")


# Searches
class Search(Base):
    __tablename__ = "searches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(Text, nullable=False)
    params = Column(JSON)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)
    status = Column(String(50), default="queued")       # queued/running/done/failed

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
    name = Column(String(191), nullable=False)          # 原来 Text，改短一点方便索引
    created_by = Column(String(100))                    # 原来无长度
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="created")      # created/running/done/failed
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
    name_en = Column(String(191), nullable=False)       # 原来 Text
    name_local = Column(String(191))                    # 原来 Text


# Regions
class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_iso3 = Column(String(3), ForeignKey("countries.iso3"))
    code = Column(String(50), nullable=False)           # 原来无长度
    name = Column(String(191), nullable=False)          # 原来 Text


# Audits
class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100), nullable=False)    # 原来 Text
    action = Column(String(50), nullable=False)         # insert/update/delete
    before = Column(JSON)
    after = Column(JSON)
    actor = Column(String(100))                         # 原来 Text
    at = Column(DateTime, default=datetime.datetime.utcnow)