import requests
from googlesearch import search
from ScraperTool import scrape_pdfs
from ScraperTool import process_pdf_link
import time



Filters = ["wikipedia","statista","worldbank","unstats","usa.ipums.org","international.ipums.org","redatam.org","ourworldindata","www.un.org","www.oecd."]
ExactTags = []
NonExactTags = ["Census", "Uganda","2018","migration"]
Filesize = None
MaxPDFs = 5
ResultsSearched = 10 # 10 IS MAX IN THIS VERSION

api_key = "PUT API KEY HERE" # API KEY
Searchcx = "f492a293c453341a1"


start = time.time()

if ExactTags != []: ExactTags = ' '.join(f'"{tag}"' for tag in ExactTags)
else: ExactTags = " "

if NonExactTags != []: NonExactTags = ' '.join(NonExactTags)
else: NonExactTags = " "

Query = ExactTags + " " + NonExactTags
url = f"https://www.googleapis.com/customsearch/v1?q={Query}&key={api_key}&cx={Searchcx}&num={ResultsSearched}"

FULL_RESULTS = []
results = []

Links = []

response = requests.get(url)
print(response.status_code)
if response.status_code == 200:
    data = response.json()
    print(data)
    # Loop over the search results
    for item in data.get('items', []):
        link = item['link']          # URL
        title = item['title']        # Title of page
        snippet = item['snippet']    # Description of page
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
            scraped = scrape_pdfs(link)
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
