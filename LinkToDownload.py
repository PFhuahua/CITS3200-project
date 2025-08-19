"""
Prototype Webscraping script:
- Makes live web requests and downloads files without checks
- Dumps selected PDF into working directory
- Changing URL and testing may result in PDFs located that are unsafe/nonexistant
"""



import re
import time
import requests
import os
from urllib.parse import urlparse

# Base URL to scrape from
url = 'https://www.homeaffairs.gov.au/research-and-statistics/statistics/visa-statistics/live/migration-program'
# Basic PDF filename filter
Filter = "2012"


start = time.time() 

# Parse the URL fetch HTML content
parsed_url = urlparse(url)
base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
response = requests.get(url)
html_content = response.text


# Find all instances of .pdf in HTML
pdf_refs = re.findall(r"\b\S+\.pdf\b", html_content, re.IGNORECASE)
for pdf in pdf_refs: print(pdf) 

# Filter out the matches
filtered = [s for s in pdf_refs if isinstance(s, str) and Filter in s]
FileSizeFilter = "data-getfilesize="
filtered = [s for s in filtered if isinstance(s, str) and FileSizeFilter not in s]
print(f"\n{len(filtered)} / {len(pdf)} PDFs match filters")

# List all filtered pdf file names and sizes
Avalible_pdfs = []
for pdf in  filtered:
    PDF_name = pdf.replace('href="', '').replace('"', '')
    response = requests.head(base_url + PDF_name)
    print("\n")
    print(PDF_name[1:])
    if 'Content-Length' in response.headers:
        size_bytes = int(response.headers['Content-Length'])

        Avalible_pdfs.append([PDF_name,size_bytes])

        size_kb = size_bytes / 1024
        print(f"PDF size: {size_bytes} bytes ({size_kb:.2f} KB)")
    else:
        print("No Content-Length header. Need to download file to check size.")


# List options to user
print("\n\nAvailable PDFs:")
for idx, (name, size) in enumerate(Avalible_pdfs, start=1):
    size_str = f"{size/1024:.2f} KB" if size else "Unknown size"
    print(f"{idx}. {os.path.basename(name)} ({size_str})")

# Ask user for PDF choice
while True:
    choice = input(f"\n(type \"quit\" to exit)\nEnter a number (1-{len(Avalible_pdfs)}) to download: \n")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(Avalible_pdfs):
            break
    if choice == "quit": exit()
    print("Invalid choice. Try again.")

# Get chosen file info and name
chosen_pdf, chosen_size = Avalible_pdfs[choice-1]
filename = os.path.basename(chosen_pdf)  

# Open and copy the PDF onto working directory with original PDF name
response = requests.get(base_url + chosen_pdf, stream=True)
with open(filename, "wb") as f:
    f.write(response.content)

print("_________________________\n")
print(f"{filename} downloaded \n")


end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")