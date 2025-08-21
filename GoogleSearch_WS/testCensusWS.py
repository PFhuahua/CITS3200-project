from googlesearch import search
from ScraperTool import scrape_pdfs
import time
start = time.time() 


Country = "USA"
Year = "1950"

filters = ["wikipedia"]

othertags = ["census","migration","data"]
othertags = ' '.join(f'"{tag}"' for tag in othertags)

Query = "\""+Country +"\" " +"\""+Year+"\" " + othertags

results = []
for link in search(Query , num_results=10):
        if not any(f in link for f in filters):
              
              if(".pdf" in link): results.append(link)
              
              else: 
                scraped = scrape_pdfs(link)
                if scraped == None: continue
                for item in scraped:
                    results.append(item["url"])
                    if len(results) > 10: break
        if len(results) > 5: break

print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(results, start=1):
    print(f"{i}. {url}")
print("\n")
end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
