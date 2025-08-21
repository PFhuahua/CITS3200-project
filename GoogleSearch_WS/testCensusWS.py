from googlesearch import search
from ScraperTool import scrape_pdfs


Country = "\"Australia\""
Year = "\"2020\""

filters = ["wikipedia"]

Query = Country + Year + "\"census\"\"migration\"\"data\""
results = []
for link in search(Query , num_results=8):
        if not any(f in link for f in filters):
              
              if(".pdf" in link): results.append(link)
              
              else: 
                scraped = scrape_pdfs(link)
                if scraped == None: continue

                for item in scraped:
                    results.append(item["url"])
        if len(results) > 4: break

print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(results, start=1):
    print(f"{i}. {url}")
print("\n")