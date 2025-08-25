from db import engine
import models

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    print("census.db is created")