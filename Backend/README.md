# Census PDF Finder API

This is the FastAPI backend for the Census PDF Finder application. It provides API endpoints to search for and download census PDFs using the existing Python scraping tools.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server:**
   ```bash
   python start_api.py
   ```
   
   Or alternatively:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API:**
   - API Base URL: `http://localhost:8000/api`
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/health`

## API Endpoints
### Libraries API
- POST `/api/libraries/`
- GET `/api/libraries/`
- PUT `/api/libraries/{id}` 
- DELETE `/api/libraries/{id}` 

### Filters API
- POST `/api/filters/` 
- GET `/api/filters/` 
- PUT `/api/filters/{id}` 
- DELETE `/api/filters/{id}` 

### Search Census Documents
```
POST /api/search
```

**Request Body:**
```json
{
  "year": "2020",
  "country": "united-states",
  "state": "california", 
  "keyword": "migration",
  "max_results": 20
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "uuid",
      "titleEnglish": "California Migration Data 2020",
      "country": "United States",
      "province": "California",
      "censusYear": 2020,
      "publicationYear": 2021,
      "authorPublisher": "Census Bureau",
      "fileSizeMB": 5.0,
      "numberOfPages": 0,
      "fileTypes": ["PDF"],
      "url": "https://example.com/census_2020_us.pdf",
      "description": "Census document found for query: migration united states california census 2020"
    }
  ],
  "total": 1,
  "searchTime": 2.3,
  "query": "migration united states california census 2020"
}
```

### Download Single Document
```
GET /api/download/{document_id}
```

**Response:**
```json
{
  "download_url": "https://example.com/census_2020_us.pdf",
  "filename": "California Migration Data 2020.pdf",
  "size_mb": 5.0
}
```

### Download Multiple Documents
```
POST /api/download/bulk
```

**Request Body:**
```json
{
  "document_ids": ["uuid1", "uuid2", "uuid3"]
}
```

**Response:** ZIP file containing the documents

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

## Frontend Integration

The frontend React application should be configured to connect to this API:

1. **Environment Variables:**
   Create a `.env.local` file in the frontend directory:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

2. **CORS Configuration:**
   The API is configured to allow requests from:
   - `http://localhost:3000`
   - `http://127.0.0.1:3000`

## Development

- The API uses in-memory caching for search results
- Search results are stored in `search_cache` dictionary
- For production, consider using a proper database
- The API integrates with existing scraping tools in `GoogleSearch_WS/` and `LinkToDownload.py`

## Error Handling

The API returns proper HTTP status codes and error messages:

- `400` - Bad Request (invalid parameters)
- `404` - Not Found (document not found)
- `500` - Internal Server Error (search/download failed)

Error responses include a `detail` field with the error message.

##Run FastAPI + MySQL with Docker
docker compose up -d --build ##Start services
docker compose ps ##Check status

docker compose exec backend python -m backend.db.create_db  ##Create database tables

access api: http://localhost:8000/docs