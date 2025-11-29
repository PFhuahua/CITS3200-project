from . import models 
from .db import engine 

if __name__ == "__main__":
    print("Creating tables in MySQL")
    models.Base.metadata.create_all(bind=engine)
    print("Tables are now created in MySQL")