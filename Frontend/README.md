# Cascading Search Frontend

A simple React frontend for the Census Document Search cascading search API.

## Features

- Search form with all cascading search parameters
- Results display in table format
- Download results as CSV
- Shows which phase (Library, Bureau, or Web) found results
- Displays search time and result count
- Clean and responsive UI

## Prerequisites

- Node.js (v20.13.1 or higher)
- Backend API running on http://localhost:8000

## Setup

1. Install dependencies:

```bash
npm install
```

2. Make sure the backend API is running:

```bash
cd ../Backend
python start_api.py
```

The API should be running on `http://localhost:8000`

3. Start the frontend development server:

```bash
npm run dev
```

4. Open your browser to `http://localhost:5173`

## Quick Start Example

Try this sample search:

- **Title (English)**: "Census of Population"
- **Country**: "Argentina"
- Leave other fields empty or fill as needed
- Click "Search"

The application will automatically cascade through Library → Bureau → Web search phases.

## Usage

### Search Form Fields

**Required fields:**

- **Title (English)**: The English title of the document
- **Country**: The country where the census was conducted

**Optional fields:**

- **Original Title**: Title in the original language
- **Province**: Province or region
- **Cite**: Citation information
- **Author/Publisher**: Publisher name
- **Volume Number**: Volume identifier (e.g., "Volume I")
- **Coloniser**: Colonial power information

### How It Works

The application performs a cascading search through three phases:

1. **Library Phase**: Searches library databases first
2. **Bureau Phase**: If no results, searches bureau databases
3. **Web Phase**: If still no results, performs a web search

Results are displayed as soon as any phase succeeds, along with:

- Which phase found the results
- Time taken to complete the search
- Number of results found

### Downloading Results

Click the "Download Results (CSV)" button to export the search results as a CSV file containing:

- Title
- URL
- Source
- Phase

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Configuration

The frontend is configured to connect to the backend API at `http://localhost:8000`.

To change this, modify the fetch URL in `src/App.jsx`:

```javascript
const response = await fetch("http://localhost:8000/api/cascading-search", {
  // ...
});
```

## Technologies Used

- React 19
- Vite 7
- Vanilla CSS (no UI libraries)
