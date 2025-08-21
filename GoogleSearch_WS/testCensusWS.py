from googlesearch import search
from ScraperTool import scrape_pdfs
from ScraperTool import process_pdf_link
import time
start = time.time() 


Country = ""
Year = ""

filters = ["wikipedia"]

othertags = ["BEVÖLKERUNG UND KULTUR Volkszählung vom 27. Mai 1970 Heft 15 Bevölkerung nach überwiegendem Lebensunterhalt und Beteiligung am Erwerbsleben"]
Exact_tags = False
Filesize = None

if Exact_tags: othertags = ' '.join(f'"{tag}"' for tag in othertags)

Query = othertags

FULL_RESULTS = []
results = []
for link in search(Query, num_results=20):
    if not any(f in link for f in filters):
        if ".pdf" in link.lower():
            # Process PDF link
            pdf_info = process_pdf_link(link)
            FULL_RESULTS.append(pdf_info)
            results.append((pdf_info["url"], pdf_info["size"]))  # store as (url, size) pair
        else:
            # Non-PDF link → scrape for PDFs
            scraped = scrape_pdfs(link)
            if scraped is None:
                continue
            for item in scraped:
                FULL_RESULTS.append(item)
                results.append((item["url"], item["size"]))  # store as (url, size) pair
                if len(results) > 10:  # break inner loop if too many
                    break
    if len(results) > 10:  # break outer loop if too many
        break

unique_results = list(set(results))


print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(unique_results, start=1):
    if url[1] == None: print(f"{i}. {url[0]} file size: UNKNOWN")
    else: print(f"{i}. {url[0]}, file size: {round(url[1]/1000,0)} KB")
print("\n")
end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
