import requests
from ScraperTool import scrape_pdfs
from ScraperTool import process_pdf_link
from AITool import generate_search_queries
import os
from dotenv import load_dotenv
import time

load_dotenv()
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")
SEARCH_ID=os.environ.get("SEARCH_ID")

Filters = ["wikipedia","statista","worldbank","unstats","usa.ipums.org","international.ipums.org","redatam.org","ourworldindata","www.un.org","www.oecd."]
ExactTags = []
NonExactTags = ["Canada Census 1956 population by specified age groups for counties and census subdivisions pdf"]
Filesize = None
MaxPDFs = 30
ResultsSearched = 5 # 5 IS MAX IN THIS VERSION

start = time.time()

if ExactTags != []: ExactTags = ' '.join(f'"{tag}"' for tag in ExactTags)
else: ExactTags = " "

if NonExactTags != []: NonExactTags = ' '.join(NonExactTags)
else: NonExactTags = " "

Query = generate_search_queries(ExactTags + " " + NonExactTags).split(", ")
print(Query)

FULL_RESULTS = []
results = []

Links = []

for i in Query:
    print(i)
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ID,
        "q": i,
        "num": ResultsSearched,
    }

    response = requests.get(url, params=params)
    #print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        #print(data)
        # Loop over the search results like your old search() loop
        for item in data.get('items', []):
            link = item['link']          # URL of the result
            title = item['title']        # Title of the page
            snippet = item['snippet']    # Short description
            if link not in Links:
                Links.append(link)
    else:
        print("Error:", response.status_code, response.text)



for link in Links:
    if not any(f in link for f in Filters):
        if ".pdf" in link.lower():
            # Process PDF link
            pdf_info = process_pdf_link(link)
            if pdf_info == None: 
                continue
            FULL_RESULTS.append(pdf_info)
            results.append((pdf_info["url"], pdf_info["size"]))  # store as (url, size) pair
        else:
            # Non-PDF link -> scrape for PDFs
            scraped = scrape_pdfs(link, i)
            if scraped is None:
                continue
            for item in scraped:
                FULL_RESULTS.append(item)
                results.append((item["url"], item["size"]))  # store as (url, size) pair
                if len(results) > MaxPDFs:  # break inner loop if too many
                    break
    if len(results) > MaxPDFs:  # break outer loop if too many
        break

unique_results = list(set(results))


print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(unique_results, start=1):
    if url[1] == None: print(f"{i}. {url[0]} file size: UNKNOWN")
    else: print(f"{i}. {url[0]}, file size: {round(url[1]/1000,0)} KB")
print("\n")

end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")