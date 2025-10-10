from AITool import rank_web_results, match_result, generate_all_queries
from Func_PDF_GoogleWS import PDF_Google_WS
from dotenv import load_dotenv
from convert_metadata_to_list import convert_file
from Func_Library import Find_Lib_Results, Find_Bur_Results,integrate_db_call
import google.generativeai as genai
import os
import time
import json

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
SEARCH_ID = os.environ.get("SEARCH_ID")
genai.configure(api_key=GOOGLE_API_KEY)

'''
Batch test flow

Args:
    inputlist: List of dictionaries read from csv file containing metadata

    numlibresults: Number of library results to return from each library search

    numburresults: Number of bureau results to return from each bureau search

    websearchresults: Number of PDF results to return from web search

    websearchamt: Number of google searches to perform

    maxworkers: Max number of parallel threads to use

Returns:
    None, results written to results.txt

'''
def testFlow(inputlist, numlibresults: int =2, numburresults: int =5, websearchresults: int =5, websearchamt: int =15, maxworkers: int =9):
    with open("results.txt", "w") as f:
        f.write("")
    count = 1
    for l in inputlist:
        print(l)
        try:
            print("Starting search number", count)
            count += 1
            start = time.time()

            # Query generation phase
            docInfo = ", ".join(f"{key}: {value}" for key, value in l.items())
            try:
                queries = generate_all_queries(docInfo)
                allqueries = json.loads(queries)
                if allqueries == []:
                    print("No queries generated, skipping to next document.")
                    raise
            except Exception as e:
                print("Error generating queries:", e)
                raise
            print(f"Generated queries: {allqueries}")

            # Library search phase
            libq = allqueries[0]
            allresults = []
            for i in libq:
                try:
                    libresponse = Find_Lib_Results(i.strip(), [l["Country"]], numlibresults, maxworkers)
                    if all(v == "" for v in libresponse.values()):
                        print("No library results found.")
                        continue
                    #print("Library results found:", libresponse)
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
                print("Library result found, written to file")
                with open("results.txt", "a") as f:
                    f.write(f"Total library time taken: {libend - start:.4f} seconds\n")
                    f.write(f"Library result for document {count-1}:\n {libresult[0]}\n {libresult[1]}\n\n")
                continue
            print("No library results found, proceeding to bureau search.")

            # Bureau search phase
            burq = allqueries[1]
            allresults = []
            for i in burq:
                try:
                    burresponse = Find_Bur_Results(i.strip(), [l["Country"]], numburresults, maxworkers)
                    if all(v == "" for v in burresponse.values()):
                        print("No bureau results found.")
                        continue
                    #print("Bureau results found:", burresponse)
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
                with open("results.txt", "a") as f:
                    f.write(f"Total bureau time taken: {burend - libend:.4f} seconds\n")
                    f.write(f"Bureau result for document {count-1}:\n {burresult[0]}\n {burresult[1]}\n\n")
                print("Bureau result found, written to file")
                continue
            print("No bureau results found, proceeding to web search.")
            
            # Web search phase
            webq = allqueries[2]
            allresults = []
            for i in webq:
                try:
                    webresponse = PDF_Google_WS(i.strip(), MaxPDFs=websearchresults, ResultsSearched=websearchamt, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
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
            with open("results.txt", "a") as f:
                f.write(f"Total web time taken: {webend - burend:.4f} seconds\n")
                f.write(f"Web results for document {count-1}:\n")
                for i, url in enumerate(webresult[:3], start=1):
                    if url[1] == None:
                        f.write(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
                    else:
                        f.write(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
        except Exception as e:
            print("An error occurred during the search flow:", e)
            continue
    return

'''
Batch test flow

Args:
    inputdict: Dictionary made from given search parameters

    numlibresults: Number of library results to return from each library search

    numburresults: Number of bureau results to return from each bureau search

    wsresults: Number of PDF results to return from web search

    wsamt: Number of google searches to perform

    maxworkers: Max number of parallel threads to use

Returns:
    List of results from each phase in order, including the time taken for debugging purposes

'''
def singleFlow(inputdict, numlibresults: int = 2, numburresults: int = 5, wsresults: int = 5, wsamt: int = 15, maxworkers: int = 9):
    endres = []
    try:
        start = time.time()
        country = [inputdict["Country"]]
        # Query generation phase
        docInfo = ", ".join(f"{key}: {value}" for key, value in inputdict.items())
        try:
            queries = generate_all_queries(docInfo)
            allqueries = json.loads(queries)
            if allqueries == []:
                print("No queries generated, skipping to next document.")
                raise
        except Exception as e:
            print("Error generating queries:", e)
            raise
        endres.append(str(allqueries))

        # Library search phase
        libq = allqueries[0]
        allresults = []
        for i in libq:
            try:
                libresponse = Find_Lib_Results(i.strip(), country, numlibresults, maxworkers)
                if all(v == "" for v in libresponse.values()):
                    print("No library results found.")
            except Exception as e:
                print("Error in library search:", e)
                libresponse = []
            allresults.append(libresponse)
        try:
            res = match_result(libq, allresults)
            libresult = json.loads(res)
        except Exception as e:
            print("Error matching library results:", e)
            raise
        libend = time.time()
        endres.append(f"Total library time taken: {libend - start:.4f} seconds")
        endres.append("\n".join(map(str, libresult)))
        if libresult != []:
            return endres
        print("No library results found, proceeding to bureau search.")

        # Bureau search phase
        burq = allqueries[1]
        allresults = []
        for i in burq:
            try:
                burresponse = Find_Bur_Results(i.strip(), country, numburresults, maxworkers)
                if all(v == "" for v in burresponse.values()):
                    print("No bureau results found.")
            except Exception as e:
                print("Error in bureau search:", e)
                burresponse = []
            allresults.append(burresponse)
        try:
            res = match_result(burq, allresults)
            burresult = json.loads(res)
        except Exception as e:
            print("Error matching bureau results:", e)
            raise
        burend = time.time()
        endres.append(f"Total bureau time taken: {burend - libend:.4f} seconds")
        endres.append(burresult.join("\n"))
        if burresult != []:
            return endres
        print("No bureau results found, proceeding to web search.")
        
        # Web search phase
        webq = allqueries[2]
        allresults = []
        for i in webq:
            try:
                webresponse = PDF_Google_WS(i.strip(), MaxPDFs=wsresults, ResultsSearched=wsamt, api_key=GOOGLE_API_KEY, Searchcx=SEARCH_ID)
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
            raise
        webend = time.time()
        endres.append(f"Total web time taken: {webend - burend:.4f} seconds")
        endres.append(webresult[:3])
        return endres
    except Exception as e:
        print("An error occurred during the search flow:", e)
        raise

# Batch test; input required: csv file with metadata
'''
# Nested list from batching program
real_input = convert_file("testcsv/custtest.csv")
testFlow(real_input)
'''

# Single test; input required: params from frontend

# Below params should come from frontend
engTitle = "The Cesnus of France - The Second Series - TomeXIII - Population"
orgTitle = "STATISTIQUE DE LA FRANCE - DEUXI�ME S�RIE - TomeXIII -POPULATION"
country = "France"
province = "N/A"
ctime = "1861"
publisher = "Strasbourg - IMPRIM�RIE ADMINISTRATIVE DE VEUVE BERGER-LEVRAULT"
volume = "XIII"
coloniser = "N/A"

numlibresults = 2 # Number of library results to return OPTIONAL
numburresults = 5 # Number of bureau results to return OPTIONAL
websearchresults = 5 # Number of PDF results to return
websearchamt = 15 # Number of google searches
maxworkers = 9 # Max number of parallel threads to use OPTIONAL

integrate_db_call()

res = singleFlow({
    "English Title": engTitle,
    "Original Title": orgTitle,
    "Country": country,
    "Province": province,
    "Cite": ctime,
    "Publisher": publisher,
    "Volume": volume,
    "Coloniser": coloniser
}, numlibresults, numburresults, websearchresults, websearchamt, maxworkers)

print(res)

with open("results.txt", "w", encoding="utf-8", newline="\n") as f:
    for i in res:
        if type(i) != list:
            f.write(i+"\n")
        else:
            for i, url in enumerate(i, start=1):
                if url[1] == None:
                    f.write(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
                else:
                    f.write(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")