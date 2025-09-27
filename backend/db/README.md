##SQLite  mysql + SQLAlchemy
python -m venv .venv
.\.venv\Scripts\Activate.ps1  #windows
source .venv/bin/activate  #Linux

pip install -r backend/db/requirements.txt

docker-compose up -d db

python -m backend.db.create_db

##mysql docker
docker exec -it db mysql -u root -p
password:3200

USE project;
SHOW TABLES; ##check tables
DESCRIBE liberies;