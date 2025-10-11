Backend Census Bureau, Library and web scraper - Quick Start Steps

**Requirements:**
1. Install Docker Desktop（Register for free）
    https://www.docker.com/products/docker-desktop

2. Set Environment Variables
    Create a .env file under the Backend/GoogleSearch_WS/ folder with the following content:

        GEMINI_API_KEY=Your_Google_API_key
        SEARCH_ID=Your_custom_search_engine_ID
    _
    Alternatively, you can manually configure Backend/GoogleSearch_WS/SysTest.py:

        load_dotenv()
        GOOGLE_API_KEY = Your_Google_API_key
        SEARCH_ID = Your_custom_search_engine_ID
        genai.configure(api_key=GOOGLE_API_KEY)
    _
    To Generate a Google API key: https://aistudio.google.com/app/apikey

    To Generate a Custom Search ID: https://developers.google.com/custom-search/v1/introduction


**Steps for Program Start:**

1. Start Docker Services
    - Open the Docker Desktop application "Docker Desktop.exe".

    - Then in Project terminal run:
        docker-compose up --build


    Docker will build the images, install dependencies and start the containers.
    Wait until you see messages like:
        [+] Running 2/2
        ✔ cits3200-project-backend  Built
        ✔ Container backend         Recreated

        backend  | INFO:     Application startup complete.      

    This means Docker has finished setting up, and you can move on to the next step.


2. Access the backend container

    - Open a new Project terminal window and run:
        docker exec -it backend bash

    # note
    You are now running inside of the docker container.
    While in the docker container your terminal prompt appears as such:
        root@<container-id>:/app#
    #


3. Build the Database tables

    - Now that the terminal is inside the docker container run:
        python -m Backend.db.create_db
    

4. Populate Database tables

    -  Open the API documentation in a web brower:
        Visit http://localhost:8000/docs

    -  Import Library data on the API UI:
        Open "[POST] /api/import-libraries,  Import Libraries" dropdown menu
        Click [Try it out]
        Then [Execute]
    
    -  Import Bureau data on the API UI:
        Open "[POST] /api/import-bureaus,   Import Bureaus" dropdown menu
        Click [Try it out]
        Then [Execute]
    
    Both data tables have been copied to your local database.
    The program is now ready to run.


5. Run System Testing

    - In the terminal inside the docker container run:
        python Backend/GoogleSearch_WS/Systests.py
    
    This will output a system test of the entire backend.