# Batch Search & Export
This branch provides a batch pipeline to process census queries from CSV and export results in the CSV and JSON formats.

## Setup
pip install -r requirements.txt

## Input Format
CSV with: `year`, `country_name` (required) + optional `state_province`, `query`

## How to Run
python structured_batch.py --input queries.csv --out exports/results.csv

## Output
	•	results.csv - Flat results with metadata
	•	results.json - Nested results grouped by query
	•	errors.json - Processing errors
	•	progress.json - Real-time progress tracking
## Options
	•	--top_k 3 - Number of candidates per query
	•	--errors errors.json - Error log path
	•	--log progress.json - Progress log path

## Status
Currently using mock data for testing the batch processing pipeline. 