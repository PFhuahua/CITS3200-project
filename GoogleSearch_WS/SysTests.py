from AITool import generate_search_queries, generate_lib_queries, rank_web_results
from Func_PDF_GoogleWS import PDF_Google_WS, LIB_Google_WS
from dotenv import load_dotenv
import google.generativeai as genai
import os
import time
import ast

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
SEARCH_ID = os.environ.get("SEARCH_ID")
genai.configure(api_key=GOOGLE_API_KEY)

def testRunWS(docInfo):
    allresults = []
    webresponse = generate_search_queries(docInfo).split(";")
    for i in webresponse:
        searchresponse = PDF_Google_WS(i.strip(), MaxPDFs=5, ResultsSearched=15, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
        if searchresponse == []:
            return
        #print(searchresponse)
        for each in searchresponse:
            if each not in allresults:
                allresults.append(each)
    #print("\nSearch Results: ",allresults)
    webrank = rank_web_results(webresponse[0], allresults).split(";")
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

# Nested list from batching program
inputList = [["Name","Title (In English)","Original title","Country","Province","Date/Year of census","Date/Year of publication","Publisher","Volume number","File size of pdf original file  (KB)","Number of Pages of Table","Number of pages of original file"],
            ["cargx_18690101_0001_76319",
                "The First Cenus of the Argentine Republic verified on the days of September 15th, 16th, and 17th, 1869",
                "PRIMER CENSO DE LA REPUBLICA ARGENTINA VERIFICADO EN LOS DIAS 15, 16 y 17 de Setiembre de 1869",
                "Argentina",
                "National Record",
                "September 15th, 16th, and 17th, 1869",
                "1872",
                "Diego G. de la Fuente - Superintendent of the Census",
                "First entry",
                "69960",
                "N/A",
                "806"]]
headerList = inputList[0]
for l in inputList[1:]:
    docInfo = {}
    for i, item in enumerate(l):
        docInfo[headerList[i]] = item
    start = time.time()
    print("Starting search...")
    iResult = testRunWS(docInfo)
    for i, url in enumerate(iResult, start=1):
        url = ast.literal_eval(url.strip())
        if url[1] == None: print(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
        else: print(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
    end = time.time()
    print(f"Process time: {end - start:.4f} seconds")
    d = input("\nPress l if you want to search library instead, any other key to continue: ")
    if d.lower() == "l":
        print("Not implemented yet")
    
