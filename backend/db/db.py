from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
#use MySQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:3200@localhost:3306/project"
)
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()