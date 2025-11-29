import requests
from ..ScraperTool import scrape_pdfs
from ..ScraperTool import process_pdf_link
import time


Filters = ["wikipedia","statista","worldbank","unstats","usa.ipums.org","international.ipums.org","redatam.org","ourworldindata","www.un.org","www.oecd.",".docx"]
ExactTags = []
NonExactTags = ["census","STATISTIQUE GÉNÉRAL DE LA FRANCE - RESULTATS STATISTIQUES DU DENOMBREMENT DE 1896 - PARIS - IMPRIMERIE NATIONALE",".pdf"]
Filesize =  None
MaxPDFs = 40
ResultsSearched = 100

api_key = "API KEY" #API KEY
Searchcx = "f492a293c453341a1"


start = time.time()

if ExactTags != []: ExactTags = ' '.join(f'"{tag}"' for tag in ExactTags)
else: ExactTags = " "

if NonExactTags != []: NonExactTags = ' '.join(NonExactTags)
else: NonExactTags = " "

Query = ExactTags + " " + NonExactTags

FULL_RESULTS = []
results = []
start_search_index = 1 # Start index of searches (1)

while start_search_index <= ResultsSearched:
    # Determine how many results to request in the search (API only allows a max of 10 per search)
    num_results = min(ResultsSearched - start_search_index + 1, 10)

    url = f"https://www.googleapis.com/customsearch/v1?q={Query}&key={api_key}&cx={Searchcx}&num={num_results}&start={start_search_index}"
    response = requests.get(url)
    print(f"Requesting results {start_search_index}-{start_search_index+num_results-1}, status:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        if int(data['searchInformation']['totalResults']) == 0: break
        for item in data.get('items', []):
            link = item['link']
            title = item['title']
            snippet = item['snippet']

            if not any(f in link for f in Filters):
                if ".pdf" in link.lower():
                    pdf_info = process_pdf_link(link)
                    if pdf_info is None:
                        continue
                    FULL_RESULTS.append([pdf_info, item])
                    results.append((pdf_info["url"], pdf_info["size"],title,snippet))
                else:
                    scraped = scrape_pdfs(link)
                    if scraped is None:
                        continue
                    for pdf in scraped:
                        FULL_RESULTS.append([pdf, item])
                        results.append((pdf["url"], pdf["size"],title,snippet))
                        if len(results) >= MaxPDFs:
                            break
            if len(results) >= MaxPDFs:
                break
    else:
        print("Error:", response.status_code, response.text)

    if len(results) >= MaxPDFs:
        break

    start_search_index += num_results  # Move to next block of results

unique_results = list(set(results))



print(f"\n\nPDF RESULTS FOR {Query}:\n")
for i, url in enumerate(unique_results, start=1):
    if url[1] == None: print(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
    else: print(f"{i}. {url[0]}, \nfile size: {url[1]} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
print("\n")

end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
