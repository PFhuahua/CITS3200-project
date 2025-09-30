from AITool import generate_search_queries, generate_lib_queries, rank_web_results, match_result, generate_all_queries
from Func_PDF_GoogleWS import PDF_Google_WS
from dotenv import load_dotenv
from convert_metadata_to_list import convert_file
from Func_Library import Find_Lib_Results, Find_Bur_Results
import google.generativeai as genai
import os
import time
import json

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
SEARCH_ID = os.environ.get("SEARCH_ID")
genai.configure(api_key=GOOGLE_API_KEY)

def testFlow(inputlist):
    for l in inputlist:
        start = time.time()
        # Query generation phase
        docInfo = ", ".join(f"{key}: {value}" for key, value in l.items())
        try:
            queries = generate_all_queries(docInfo)
            allqueries = json.loads(queries)
            if allqueries == []:
                print("No queries generated, skipping to next document.")
                continue
        except Exception as e:
            print("Error generating queries:", e)
            continue
        print(f"Generated queries: {allqueries}")

        # Library search phase
        libq = allqueries[0]
        allresults = []
        for i in libq:
            try:
                libresponse = Find_Lib_Results(i.strip())
                if libresponse == []:
                    print("No library results found.")
                    continue
            except Exception as e:
                print("Error in library search:", e)
                libresponse = []
            allresults.append(libresponse)
        try:
            res = match_result(libq, allresults)
            libresult = json.loads(res)
        except Exception as e:
            print("Error matching library results:", e)
            continue
        libend = time.time()
        print(f"Total library time taken: {libend - start:.4f} seconds")
        if libresult != []:
            print(f"Library result found: {libresult}")
            continue

        # Bureau search phase
        burq = allqueries[1]
        allresults = []
        for i in burq:
            try:
                burresponse = Find_Bur_Results(i.strip())
                if burresponse == []:
                    print("No bureau results found.")
                    continue
            except Exception as e:
                print("Error in bureau search:", e)
                burresponse = []
            allresults.append(burresponse)
        try:
            res = match_result(burq, allresults)
            burresult = json.loads(res)
        except Exception as e:
            print("Error matching bureau results:", e)
            continue
        burend = time.time()
        print(f"Total bureau time taken: {burend - libend:.4f} seconds")
        if burresult != []:
            print(f"Bureau result found: {burresult}")
            continue
        
        # Web search phase
        webq = allqueries[2]
        allresults = []
        for i in webq:
            try:
                webresponse = PDF_Google_WS(i.strip(), MaxPDFs=5, ResultsSearched=15, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
                if webresponse == []:
                    print("No web results found.")
                    continue
            except Exception as e:
                print("Error in web search:", e)
                webresponse = []
            allresults.append(webresponse)
        try:
            res = rank_web_results(webq[0], allresults)
            webresult = json.loads(res)
            print("Web results matched")
        except Exception as e:
            print("Error matching web results:", e)
            continue
        webend = time.time()
        print(f"Total web time taken: {webend - burend:.4f} seconds")
        for i, url in enumerate(webresult[:3], start=1):
            if url[1] == None:
                print(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
            else:
                print(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
    return


def testRunWS(docInfo):
    allresults = []
    try:
        res = generate_search_queries(docInfo)
        #print(res)
        webresponse = json.loads(res)
    except json.JSONDecodeError as e:
        print("JSON decode error in webresponse:", e)
        return f'["{e}"]'
    for i in webresponse:
        searchresponse = PDF_Google_WS(i.strip(), MaxPDFs=5, ResultsSearched=15, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
        if searchresponse == []:
            return '["Error: No results found"]'
        #print(i, searchresponse)
        for each in searchresponse:
            if each not in allresults:
                allresults.append(each)
    #print("\nSearch Results: ",allresults)
    webrank = rank_web_results(webresponse[0], allresults)
    #print(webrank)
    return webrank

def testRunLib(docInfo):
    try:
        res = generate_lib_queries(docInfo)
        libresponse = json.loads(res)
        print(libresponse)
    except json.JSONDecodeError as e:
        print("JSON decode error in libresponse:", e)
        return f'["{e}"]'
    allresults = []
    for i in libresponse:
        searchresponse = Find_Lib_Results(i.strip())
        allresults.append(searchresponse)
        #print("\nLibrary Search Results: ",searchresponse)
    libresult = match_result(libresponse, allresults)
    return libresult

def testws(real_input):
    count = 1
    all_time = []
    for l in real_input:
        docInfo = ", ".join(f"{key}: {value}" for key, value in l.items())
        start = time.time()
        print(f"Starting search number {count}...")
        count += 1
        iResult = testRunWS(docInfo)
        try:
            ranked_results = json.loads(iResult)
        except Exception as e:
            print("Error converting iResult:", e)
            print(iResult)
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
        '''d = input("\nPress l if you want to search library instead, any other key to continue: ")
        if d.lower() == "l":
            print("Not implemented yet")'''
    print(f"\nAverage time per document: {sum(all_time)/len(all_time):.4f} seconds")

def testlib(real_input):
    count = 1
    all_time = []
    for l in real_input:
        docInfo = ", ".join(f"{key}: {value}" for key, value in l.items())
        start = time.time()
        print(f"Starting library search number {count}...")
        count += 1
        iResult = testRunLib(docInfo)
        try:
            ranked_results = json.loads(iResult)
        except Exception as e:
            print("Error converting iResult:", e)
            print(iResult)
            continue
        print(ranked_results)
        end = time.time()
        all_time.append(end - start)
        print(f"Process time: {end - start:.4f} seconds")
        '''with open("search_results.txt", "a", encoding="utf-8") as file:
            file.write(f"\nResults for document: {l['Name']}")
            file.write(f"\nResults for document: {l['Title (In English)']}")
            file.write(f"\nTime taken: {end - start:.4f}\n\n")
            for i, url in enumerate(ranked_results[:3], start=1):
                if url[1] == None:
                    file.write(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
                else:
                    file.write(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
        print(f"Results for document: {l['Name']} written to search_results.txt")'''
    print(f"\nAverage time per lib search: {sum(all_time)/len(all_time):.4f} seconds")

with open("search_results.txt", "w", encoding="utf-8") as file:
    file.write("")

# Nested list from batching program
real_input = convert_file("testcsv/custtest.csv")
testFlow(real_input)