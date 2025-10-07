import requests
import time

Filters = [".docx"]
ExactTags = []
NonExactTags = ["SEGUNDO  CENSO DE LA REPUBLICA ARGENTINA TOMO III Y ULTIMO 1895"]
MaxHTML = 10
ResultsSearched = 10

api_key = "" #API KEY
Searchcx = "97c19d00f487341b6"


start = time.time()

if ExactTags != []: ExactTags = ' '.join(f'"{tag}"' for tag in ExactTags)
else: ExactTags = " "

if NonExactTags != []: NonExactTags = ' '.join(NonExactTags)
else: NonExactTags = " "

Query = ExactTags + " " + NonExactTags

FULL_RESULTS = []
results = []
start_search_index = 0 # Start index of searches (1)

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
            print(f"\n{link}\n")
            title = item['title']
            snippet = item['snippet']

            if not any(f in link for f in Filters):
                print(link)
                results.append([link,title,snippet])
            if len(results) >= MaxHTML:
                break
    else:
        print("Error:", response.status_code, response.text)
    
    if len(results) >= MaxHTML:
        break
    
    start_search_index += num_results  # Move to next block of results


print(f"\n\nLibrary RESULTS FOR {Query}:\n")
for i, url in enumerate(results, start=1):
    print(f"{i}. {url[0]} \nTitle: {url[1]}, \nsnippet: {url[2]}\n")
print("\n")

end = time.time()
print(f"Elapsed time: {end - start:.4f} seconds")
