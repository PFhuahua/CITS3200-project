# Cascading Search Feature - Setup Guide

## Overview

This guide will help you set up and run the new cascading search feature that searches for census documents across libraries, bureaus, and the web.

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ and npm (for frontend)
- MySQL database running
- Google Gemini API key
- Google Custom Search Engine ID

## Backend Setup

### 1. Environment Configuration

Create a `.env` file in the `Backend/` directory:

```bash
cd Backend
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
SEARCH_ID=your_google_search_engine_id_here
DATABASE_URL=mysql://root:@localhost/project
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

For windows PowerShell:
```bash
cd Backend
@"
GEMINI_API_KEY=your_gemini_api_key_here
SEARCH_ID=your_google_search_engine_id_here
DATABASE_URL=mysql://root:@localhost/project
API_HOST=0.0.0.0
API_PORT=8000
"@ | Set-Content .env
```


### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

Make sure your MySQL database is running and initialized:

```bash
cd db
python create_db.py
python seed.py
cd ..
```

### 4. Import Libraries and Bureaus

```bash
# Start the API server
python start_api.py

# In another terminal, import data
curl -X POST http://localhost:8000/api/import-libraries
curl -X POST http://localhost:8000/api/import-bureaus
```

### 5. Verify Backend

```bash
curl http://localhost:8000/api/health
```

You should see:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-10T...",
  "version": "1.0.0"
}
```

## Frontend Setup

### 1. Environment Configuration (Optional)

Create a `.env` file in the `Frontend/` directory if you need to customize the API URL:

```bash
cd Frontend
echo "VITE_API_URL=http://localhost:8000" > .env
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend should now be running at `http://localhost:5173`

## Using the Cascading Search

### Access the Feature

1. Open your browser to `http://localhost:5173`
2. Click "Advanced Search" in the navigation menu
3. Or navigate directly to `http://localhost:5173/cascading-search`

### Fill Out the Form

**Required Fields:**

- **English Title**: e.g., "Census of France - Volume XIII"
- **Country**: e.g., "France"

**Optional Fields:**

- **Original Title**: e.g., "STATISTIQUE DE LA FRANCE..."
- **Province/State**: e.g., "Île-de-France"
- **Census Year**: e.g., "1861"
- **Publisher**: e.g., "Government Printing Office"
- **Volume Number**: e.g., "XIII"
- **Coloniser**: e.g., "N/A"

**Advanced Settings** (optional):

- Library Results: 1-10 (default: 2)
- Bureau Results: 1-10 (default: 5)
- Web Results: 1-20 (default: 5)
- Web Search Amount: 5-30 (default: 15)
- Max Workers: 1-20 (default: 9)

### Submit and View Results

1. Click the "Search" button
2. Watch the progress indicator as it searches through:
   - National Libraries
   - Statistical Bureaus
   - Web Search
3. View results when found
4. Click "Open Document" or "View in [Source]" to access the document

## API Endpoints

### Health Check

```bash
GET /api/health
```

### Cascading Search

```bash
POST /api/cascading-search
Content-Type: application/json

{
  "englishTitle": "Census of France",
  "country": "France",
  "cite": "1861"
}
```

### Libraries Management

```bash
# List all libraries
GET /api/libraries/

# Create library
POST /api/libraries/

# Update library
PUT /api/libraries/{id}

# Delete library
DELETE /api/libraries/{id}
```

### Bureaus Management

```bash
# List all bureaus
GET /api/bureaus/

# Create bureau
POST /api/bureaus/

# Update bureau
PUT /api/bureaus/{id}

# Delete bureau
DELETE /api/bureaus/{id}
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or change the port in .env
API_PORT=8001
```

**Database connection failed:**

```bash
# Check MySQL is running
mysql -u root -p -e "SHOW DATABASES;"

# Verify database exists
mysql -u root -p -e "USE project; SHOW TABLES;"
```

**Import errors:**

```bash
# Make sure you're in the Backend directory
cd Backend

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Frontend Issues

**Build errors:**

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**

```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS settings in Backend/api.py
# Make sure port 5173 is in the allow_origins list
```

### Search Issues

**No results found:**

- Try simpler search terms
- Remove optional fields
- Check that libraries/bureaus are imported
- Verify API keys are correct

**Search too slow:**

- Reduce max_workers
- Reduce wsAmt (web search amount)
- Check internet connection
- Review backend logs for errors

**AI query generation fails:**

- Verify GEMINI_API_KEY is set correctly
- Check API quota limits
- Review backend logs for detailed errors

## Development

### Running Tests

Backend:

```bash
cd Backend/GoogleSearch_WS
python SysTests.py
```

### Adding New Libraries

1. Prepare library configuration JSON
2. POST to `/api/libraries/`
3. Verify with GET `/api/libraries/`

Example:

```bash
curl -X POST http://localhost:8000/api/libraries/ \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "New National Library",
    "URL_Start": "https://...",
    "SearchSelector": "...",
    "Country": "CountryName",
    ...
  }'
```

### Code Structure

```
CITS3200-project/
├── Backend/
│   ├── api.py                    # FastAPI application with endpoints
│   ├── GoogleSearch_WS/
│   │   ├── AITool.py            # AI query generation & ranking
│   │   ├── Func_Library.py      # Library/Bureau search functions
│   │   ├── Func_PDF_GoogleWS.py # Web search functions
│   │   └── SysTests.py          # Test flow (reference implementation)
│   └── db/
│       └── models.py            # Database models
├── Frontend/
│   └── src/
│       ├── components/
│       │   ├── cascading-search/    # Search components
│       │   └── Navigation.tsx       # Navigation menu
│       ├── pages/
│       │   └── CascadingSearchPage.tsx  # Main page
│       └── services/
│           └── cascadingSearchApi.ts    # API client
└── CASCADING_SEARCH_SETUP.md   # This file
```

## Production Deployment

### Backend

1. Set environment variables in production environment
2. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
   ```
3. Set up proper database credentials
4. Enable HTTPS
5. Configure proper CORS origins

### Frontend

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `dist/` folder with a web server (nginx, Apache, etc.)
3. Update VITE_API_URL to production backend URL
4. Enable HTTPS

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review backend logs: `Backend/api.log` (if configured)
3. Check browser console for frontend errors
4. Review the comprehensive documentation in `Frontend/CASCADING_SEARCH.md`

## Example Full Workflow

```bash
# 1. Start backend
cd Backend
python start_api.py &

# 2. Import data (first time only)
curl -X POST http://localhost:8000/api/import-libraries
curl -X POST http://localhost:8000/api/import-bureaus

# 3. Start frontend
cd ../Frontend
npm run dev

# 4. Open browser
open http://localhost:5173/cascading-search

# 5. Search for a document
# Fill in form with:
#   English Title: "Census of France 1861"
#   Country: "France"
# Click "Search"
# Wait for results
```

That's it! You should now have the cascading search feature up and running.
