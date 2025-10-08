##SQLite  mysql + SQLAlchemy

1.System Requirements
 Install Docker Desktop（Register for free）
https://www.docker.com/products/docker-desktop

2.Project Structure
CITS3200-project/
├─ Backend/
│ ├─ api.py ← FastAPI entry point
│ ├─ db/
│ │ ├─ db.py
│ │ ├─ models.py
│ ├─ data/
│ │ └─ libraries.json ← Import data file
├─ docker-compose.yml
├─ requirements.txt
└─ README.md

3.Start Docker services
docker-compose up --build
When you see
Uvicorn running on http://0.0.0.0:8000,
your backend is ready.


4.Open the API documentation
Visit http://localhost:8000/docs in your browser.


5.Import database data (libraries.json)
In Swagger UI, find POST /api/import-libraries

Click “Try it out” → “Execute”

It will read backend/data/libraries.json and insert all records into MySQL.



Method	Endpoint	Description
POST	/api/libraries/	Create a library record
GET	/api/libraries/	List all libraries
PUT	/api/libraries/{id}	Update one record
DELETE	/api/libraries/{id}	Delete one record
POST	/api/filters/	Add a filter link
GET	/api/filters/	View all filter links
DELETE	/api/filters/{id}	Delete a filter link

In the /docs page, click the corresponding interface → “Try it out” to operate directly.

6.Viewing MySQL database contents
##in a new terminal

docker exec -it db mysql -u root -p
password：3200

USE project;
SHOW TABLES;
SELECT * FROM libraries LIMIT 10;



##Each team member runs an independent container environment.

###The database is stored in their own mysql_data folder.

###Code changes take effect immediately within the container.

###There is no impact on other teams.

7.LAN access
http://localhost:8000 is only valid on this computer. Only the computer running the service can access it through localhost.

Teammates can access your host IPv4 address: http://<your IPv4>:8000  ##unifi does not seem to allow LAN access

Others access the database instance connected to the backend running on the local machine.This means that all they see/modify is the data on your machine; it won't affect their own local database unless they also start their own container pointing to the same remote database.


What we can do in the future:
Deploy the service to a cloud server and use permission control and backup strategies.






python -m venv .venv  ##No need Docker is an isolated environment 
.\.venv\Scripts\Activate.ps1  #windows
source .venv/bin/activate  #Linux

pip install -r backend/db/requirements.txt ##No need to manually pip install any packages

##for add table
docker-compose down -v && docker-compose up --build  ##Delete old data and rebuild the database

##mysql docker
docker exec -it db mysql -u root -p
password:3200

USE project;
SHOW TABLES; ##check tables
DESCRIBE liberies;



UPDATE:The POST interface of /api/libraries/ has been enhanced
Pydantic's alias mechanism allows "Name" and "name" to be mixed

{
  "name": "University of Texas Libraries",
  "url_start": "https://search.lib.utexas.edu/discovery/search?query=any,contains,",
  "url_end": "&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
  "search_selector": "div.result-item-image",
  "attribute": {
    "ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"
  },
  "tag": "h3",
  "tag_class": "item-title",
  "result_selector": "div.bar.alert-bar",
  "result_url_start": "",
  "visible": true,
  "priority": 1,
  "country": "Texas",
  "captcha": false
}


{
  "Texas": {
    "Name": "University of Texas Libraries",
    "URL_Start": "https://search.lib.utexas.edu/discovery/search?query=any,contains,",
    "URL_End": "&tab=Everything&vid=01UTAU_INST:SEARCH&offset=0&radios=resources&mode=simple",
    "SearchSelector": "div.result-item-image",
    "Attribute": {
      "ng-class": "::{'full-view-mouse-pointer':$ctrl.isFullView}"
    },
    "tag": "h3",
    "tag_class": "item-title",
    "ResultSelector": "div.bar.alert-bar",
    "Result_URL_Start": "",
    "Visible": true,
    "Priority": 1,
    "CAPTCHA": false
  }
}##The system automatically recognizes the outer layer "Texas" as the value of the Country field


POST /api/bureaus/ supports exactly the same structure, field naming conventions, and behavior.



In addition to importing individual records via POST /api/libraries/ in Swagger, you can also add new data structures directly to an existing JSON file (e.g., libraries.json) and then call /api/import-libraries to import them all at once.










1·Database access instructions Func_Library.py has been updated
Need to run python in the backend docker
docker exec -it backend bash

Load all data at once



from backend.GoogleSearch_WS.Func_Library import integrate_db_call

library_dict, bureau_dict = integrate_db_call()
# Example usage
print(library_dict["France"])         
print(bureau_dict["Australia"])   


Suitable for:
You need to process all countries at once (e.g., for batch export or analysis).
You don't need to update the database in real time while the application is running.


Query by country dynamics
This method supports writing Library["France"] directly, just like before. When accessed, it will automatically connect to the database, query the corresponding country data, and return it as a dictionary.


from backend.GoogleSearch_WS.Func_Library import Library, Bureau

lib_data = Library["France"]     # Automatically fetches France from DB
bur_data = Bureau["France"]

print(lib_data["url_start"])
print(bur_data["search_selector"])



You just need data for one country (e.g. Library["France"]).
You want the data to be always up-to-date in real time.
You can import both Library and integrate_db_call() at the same time without conflict.