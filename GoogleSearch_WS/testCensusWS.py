from googlesearch import search
from ScraperTool import scrape_pdfs
import time
start = time.time() 


Country = ""
Year = ""

filters = ["wikipedia"]

othertags = ["SEGUNDO CENSO DE LA REPUBLICA ARGENTINA MAYO 10 DE 1895 368 PRIMEROS RESULTADOS MAYO 10 DE 1896 COMISIÓN DIRECTIVA: DIEGO G.. DE LA FUENTE, Presidente. GABRIEL. CARRASCO- ALBERTO B. MARTiNEZ Vocales,"]
othertags = ' '.join(f'"{tag}"' for tag in othertags)

Query = othertags

results = []
for link in search(Query , num_results=5):
        if not any(f in link for f in filters):
              
              if(".pdf" in link): results.append(link)
              
              else: 
                scraped = scrape_pdfs(link)
                if scraped == None: continue
                for item in scraped:
                    results.append(item["url"])
                    if len(results) > 10: break
        if len(results) > 5: break

unique_results = list(set(results))


print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(unique_results, start=1):
    print(f"{i}. {url}")
print("\n")
end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
