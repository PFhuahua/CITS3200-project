# Batch Search Feature Guide

## Overview

The batch search feature allows you to upload a CSV file containing multiple census documents and perform cascading searches for all of them in parallel. This is useful for processing large datasets of census documents efficiently.

## Features

- **CSV Upload**: Upload a CSV file with multiple census document records
- **Parallel Processing**: Searches are performed in parallel (up to 5 concurrent searches)
- **Progress Tracking**: Real-time status updates for each search
- **Results Summary**: View statistics including successful/failed searches and total time
- **CSV Export**: Download batch results as a CSV file
- **Cascading Search**: Each row uses the full cascading search (Library → Bureau → Web)

## CSV Format Requirements

### Required Columns

- `Title (In English)` - The English title of the census document
- `Country` - The country name

### Optional Columns

- `Original title` - Title in the original language
- `Province` - Province or state name
- `Date/Year of census` - The year the census was taken
- `Author/Publisher` - Publisher or author information
- `Volume number (if applicable)` - Volume number if applicable
- `Colonising power` - Colonial power if applicable

### Example CSV Format

```csv
Table Name:,Name,Title (In English),Original title,Country,Province,Date/Year of census,Date/Year of Publication,Author/Publisher,Volume number (if applicable),File size of pdf original file  (KB),Number of Pages of Table,Number of pages of original file,Colonising power,,Meta Data Log of Tables collected,N/A: Not Available
N/A,cargx_18690101_0001_76319,"The First Cenus of the Argentine Republic verified on the days of September 15th, 16th, and 17th, 1869","PRIMER CENSO DE LA REPUBLICA ARGENTINA VERIFICADO EN LOS DIAS 15, 16 y 17 de Setiembre de 1869",Argentina,National Record,"September 15th, 16th, and 17th, 1869",1872,Diego G. de la Fuente - Superintendent of the Census,First entry,69960,N/A,806,Spain,,,
N/A,cfra_18460101_0001_76681,The Cesnus of France - The Second Series - TomeXIII - Population,STATISTIQUE DE LA FRANCE - DEUXIÈME SÉRIE - TomeXIII -POPULATION,France,National Record,1861,N/A,Strasbourg - IMPRIMERIE ADMINISTRATIVE DE VEUVE BERGER-LEVRAULT,Second Series - Tome XIII,147588,N/A,460,N/A,,,
```

## How to Use

### 1. Access the Batch Search Tab

1. Start the backend server (if not already running):

   ```bash
   cd Backend
   python start_api.py
   ```

2. Start the frontend (if not already running):

   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser to `http://localhost:5173`
4. Click on the **📊 Batch Search** tab in the navigation

### 2. Upload Your CSV File

1. Click the **"Choose CSV File"** button
2. Select your CSV file from your computer
3. The file name will appear on the button once selected

### 3. Start the Batch Search

1. Click the **"Start Batch Search"** button
2. Wait for the searches to complete (this may take several minutes depending on the number of rows)
3. You'll see a progress message: "Processing batch search..."

### 4. View Results

Once complete, you'll see:

- **Summary Statistics**:

  - Total Rows processed
  - Successful searches (✅)
  - Failed searches (❌)
  - Total time taken

- **Results Table** showing for each row:
  - Row number
  - Title
  - Country
  - Search phase (Library/Bureau/Web)
  - Status (Success/Failed/No Results)
  - Result links (clickable links to documents)

### 5. Download Results

Click the **"📥 Download Results (CSV)"** button to export the results to a CSV file.

The exported CSV will include:

- Row number
- Title
- Country
- Phase
- Status
- Result URL
- Error message (if any)

## API Endpoint

### POST `/api/batch-search`

**Description**: Performs cascading search on multiple rows from a CSV file.

**Request**:

- Content-Type: `multipart/form-data`
- Body: CSV file with the required format

**Response**:

```json
{
  "total_rows": 10,
  "successful_searches": 8,
  "failed_searches": 2,
  "results": [
    {
      "row_number": 1,
      "search_input": {
        "english_title": "Census of Argentina 1869",
        "country": "Argentina",
        "original_title": "...",
        ...
      },
      "search_result": {
        "phase": "library",
        "queries": ["..."],
        "results": [[...]],
        "time_taken": 5.23,
        "status": "success"
      },
      "error": null
    },
    ...
  ],
  "total_time_taken": 45.67
}
```

## Performance Considerations

### Parallel Processing

- The system processes up to **5 searches in parallel** by default
- This balances speed with API rate limits and system resources
- Adjust `max_workers` in the backend code if needed

### API Rate Limits

- The Gemini API has rate limits that may affect batch processing
- If you encounter rate limit errors, consider:
  - Reducing the number of rows processed at once
  - Adding delays between batches
  - Using a higher-tier API plan

### Processing Time

- Each search goes through 3 phases (Library → Bureau → Web)
- Average time per search: 10-30 seconds
- For 100 rows: expect 20-60 minutes total processing time

## Troubleshooting

### Error: "No valid rows found in CSV file"

- Check that your CSV has the required columns: "Title (In English)" and "Country"
- Ensure there are no extra header rows
- Verify the CSV encoding is UTF-8

### Error: "GEMINI_API_KEY not configured"

- Set the GEMINI_API_KEY environment variable in Backend/.env
- Restart the backend server

### Some searches fail with "Invalid query format"

- This indicates an issue with the AI query generation
- Check your Gemini API key is valid
- Verify the API quota hasn't been exceeded

### Searches are very slow

- This is normal for large batches
- The cascading search tries multiple sources per document
- Consider processing smaller batches if time is a concern

### CSV upload fails

- Ensure the file is a valid CSV (not Excel .xlsx)
- Check the file size (very large files may timeout)
- Verify the CSV encoding is UTF-8

## Sample Data

You can use the test data provided in the repository:

```
Backend/GoogleSearch_WS/testcsv/test_data.csv
```

This file contains 96 sample census records you can use to test the batch search feature.

## Tips for Best Results

1. **Start Small**: Test with 5-10 rows first to verify the CSV format
2. **Clean Your Data**: Ensure titles and countries are accurate
3. **Use Original Titles**: Including original titles improves search accuracy
4. **Include Years**: Adding census years helps narrow down results
5. **Monitor Progress**: Watch the console/network tab for any errors
6. **Save Results**: Download the CSV results for record-keeping

## Advanced Usage

### Customizing Search Parameters

Currently, the batch search uses default parameters:

- Library Results: 2
- Bureau Results: 5
- Web Results: 5
- Web Search Amount: 15
- Max Workers: 9

To customize these, you'll need to modify the `perform_single_cascading_search` function in `Backend/api.py`.

### Processing Large Batches

For very large CSV files (>100 rows):

1. Split the CSV into smaller batches
2. Process each batch separately
3. Combine the results using the CSV downloads
4. This prevents timeouts and makes error recovery easier

## Support

For issues or questions:

1. Check the backend logs for detailed error messages
2. Review the browser console for frontend errors
3. Verify your API keys are correct
4. Ensure the database is properly initialized with libraries and bureaus

## Example Workflow

1. **Prepare your CSV**

   - Export your census metadata to CSV
   - Ensure it has the required columns
   - Save as UTF-8 encoded

2. **Upload and Process**

   - Navigate to Batch Search tab
   - Upload your CSV file
   - Click Start Batch Search
   - Wait for completion

3. **Review Results**

   - Check the summary statistics
   - Review individual results in the table
   - Click on result links to verify documents

4. **Export and Save**
   - Download the results CSV
   - Save for your records
   - Use for further processing or analysis

Enjoy efficient batch processing of your census document searches!
