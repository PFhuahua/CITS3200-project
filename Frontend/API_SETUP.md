# API Integration Setup Guide

This guide explains how to connect the React frontend to the Python backend API.

## Prerequisites

1. **Backend Setup:**
   - Navigate to the backend directory: `cd ../CITS3200-project/Backend`
   - Install dependencies: `pip install -r requirements.txt`
   - Start the API server: `python start_api.py`
   - Verify the API is running: Visit `http://localhost:8000/docs`

2. **Frontend Setup:**
   - The frontend is already configured to connect to `http://localhost:8000/api`
   - If you need to change the API URL, create a `.env.local` file:
     ```
     VITE_API_BASE_URL=http://localhost:8000/api
     ```

## Running the Application

1. **Start the Backend API:**
   ```bash
   cd ../CITS3200-project/Backend
   python start_api.py
   ```

2. **Start the Frontend:**
   ```bash
   cd census-pdf-finder
   npm run dev
   ```

3. **Verify Connection:**
   - The API status indicator in the top-right corner should show "API Online"
   - Try searching for census documents
   - Test download functionality

## API Endpoints

The frontend now uses these API endpoints:

- `POST /api/search` - Search for census documents
- `GET /api/download/{id}` - Download a single document
- `POST /api/download/bulk` - Download multiple documents as ZIP
- `GET /api/health` - Health check

## Troubleshooting

1. **API Offline:**
   - Check if the backend server is running on port 8000
   - Verify no firewall is blocking the connection
   - Check the backend logs for errors

2. **CORS Errors:**
   - The API is configured to allow requests from localhost:3000
   - If you're using a different port, update the CORS settings in `api.py`

3. **Search Not Working:**
   - Check the browser console for error messages
   - Verify the search parameters are being sent correctly
   - Check the backend logs for search errors

## Development Notes

- The API now uses real web scraping with your existing GoogleSearch_WS tools
- Search results are cached in memory (not persistent across server restarts)
- Download functionality returns actual PDF URLs found by the scraper
- The system integrates with googlesearch-python for Google search functionality
