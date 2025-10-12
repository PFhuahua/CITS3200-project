from sqlalchemy import (
    Column, String, Integer, Date, DateTime, Text,
    ForeignKey, JSON, Float, Boolean
)
from sqlalchemy.orm import relationship
from Backend.db.db import Base
import datetime


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False, index=True)     
    url_start = Column(String(500), nullable=False)   
    url_end = Column(String(500)) 
    result_url_start = Column(String(500))                      
    search_selector = Column(String(200), nullable=False)
    attribute = Column(JSON)                        
    tag = Column(String(50))
    tag_class = Column(String(100))
    result_selector = Column(String(200))
    visible = Column(Boolean, default=True)
    priority = Column(Integer, default=1, index=True)
    country = Column(String(100), index=True, nullable=False)
    captcha = Column(Boolean, default=False)   

class Bureau(Base):
    __tablename__ = "bureaus"
       
       
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), nullable=False, index=True)     
    url_start = Column(String(500), nullable=False)   
    url_end = Column(String(500)) 
    result_url_start = Column(String(500))                      
    search_selector = Column(String(200), nullable=False)
    attribute = Column(JSON)                        
    tag = Column(String(50))
    tag_class = Column(String(100))
    result_selector = Column(String(200))
    visible = Column(Boolean, default=True)
    priority = Column(Integer, default=1, index=True)
    country = Column(String(100), index=True, nullable=False)
    captcha = Column(Boolean, default=False)   
class FilterLink(Base):
    __tablename__ = "filter_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(500), nullable=False) 