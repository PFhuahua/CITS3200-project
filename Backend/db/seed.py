# seed.py for testing
from db import SessionLocal
from models import Source, Document, Country
import datetime

db = SessionLocal()
try:
    db.merge(Country(iso2="AU", iso3="AUS", m49=36,
                     name_en="Australia", name_local="Australia"))

    src = Source(name="ABS", type="gov_site", homepage_url="https://www.abs.gov.au")
    db.add(src)
    db.flush()  

    # 
    doc = Document(
        source_id=src.id,
        title="Census 2021 Highlights",
        url="https://example.com/abs-census-2021",
        published_at=datetime.date(2021, 6, 30),
        lang="en",
        country_iso3="AUS",
        status="active"
    )
    db.add(doc)

    db.commit()
    print("Seed inserted. source_id =", src.id, "document_id =", doc.id)
finally:
    db.close()
