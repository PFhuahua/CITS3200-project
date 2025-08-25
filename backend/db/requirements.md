SQLite + SQLAlchemy
python -m venv .venv
.\.venv\Scripts\Activate.ps1  #windows
source .venv/bin/activate  #Linux

pip install -r backend/db/requirements.txt

python -m backend.db.create_db