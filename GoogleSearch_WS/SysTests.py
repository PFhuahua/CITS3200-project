from AITool import generate_search_queries, generate_lib_queries, rank_web_results
from Func_PDF_GoogleWS import PDF_Google_WS, LIB_Google_WS
from dotenv import load_dotenv
from convert_metadata_to_list import convert_file
import google.generativeai as genai
import os
import time
import json

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
SEARCH_ID = os.environ.get("SEARCH_ID")
genai.configure(api_key=GOOGLE_API_KEY)

def testRunWS(docInfo):
    allresults = []
    try:
        res = generate_search_queries(docInfo)
        #print(res)
        webresponse = json.loads(res)
    except json.JSONDecodeError as e:
        print("JSON decode error in webresponse:", e)
        return
    for i in webresponse:
        searchresponse = PDF_Google_WS(i.strip(), MaxPDFs=5, ResultsSearched=15, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
        if searchresponse == []:
            return
        #print(i, searchresponse)
        for each in searchresponse:
            if each not in allresults:
                allresults.append(each)
    #print("\nSearch Results: ",allresults)
    webrank = rank_web_results(webresponse[0], allresults)
    #print(webrank)
    return webrank

def testRunLib(docInfo):
    allresults = []
    libresponse = generate_lib_queries(docInfo).split(";")
    for i in libresponse:
        searchresponse = LIB_Google_WS(i.strip(), MaxHTML=5, ResultsSearched=5, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
        if searchresponse == []:
            continue
        print("\nLibrary Search Results: ",searchresponse)
    
    webresponse = generate_search_queries(docInfo).split(";")
    for i in webresponse:
        searchresponse = PDF_Google_WS(i.strip(), MaxPDFs=5, ResultsSearched=5, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
        if searchresponse == []:
            return
        for each in searchresponse:
            if each not in allresults:
                allresults.append(each)
    print("\nSearch Results: ",allresults)
    webrank = rank_web_results(webresponse[0], allresults).split(";")
    return webrank

with open("search_results.txt", "w", encoding="utf-8") as file:
    file.write("")

# Nested list from batching program
real_input = convert_file("test_data.csv")
count = 1
all_time = []
for l in real_input:
    docInfo = ", ".join(f"{key}: {value}" for key, value in l.items())
    start = time.time()
    print(f"Starting search number {count}...")
    iResult = testRunWS(docInfo)
    try:
        ranked_results = json.loads(iResult)
    except Exception as e:
        print("Error converting iResult:", e)
        print(str(iResult))
        continue
    #print(iResult)
    end = time.time()
    all_time.append(end - start)
    print(f"Process time: {end - start:.4f} seconds")
    with open("search_results.txt", "a", encoding="utf-8") as file:
        file.write(f"\nResults for document: {l['Name']}")
        file.write(f"\nResults for document: {l['Title (In English)']}")
        file.write(f"\nTime taken: {end - start:.4f}\n\n")
        for i, url in enumerate(ranked_results[:3], start=1):
            if url[1] == None:
                file.write(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
            else:
                file.write(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
    print(f"Results for document: {l['Name']} written to search_results.txt")
    count += 1
    '''d = input("\nPress l if you want to search library instead, any other key to continue: ")
    if d.lower() == "l":
        print("Not implemented yet")'''
print(f"\nAverage time per document: {sum(all_time)/len(all_time):.4f} seconds")