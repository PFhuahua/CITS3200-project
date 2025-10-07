from AITool import rank_web_results, match_result, generate_all_queries
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
    count = 1
    for l in inputlist:
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
                    libresponse = Find_Lib_Results(i.strip())
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
                print(f"Library result found: {libresult}")
                continue
            print("No library results found, proceeding to bureau search.")

            # Bureau search phase
            burq = allqueries[1]
            allresults = []
            for i in burq:
                try:
                    burresponse = Find_Bur_Results(i.strip())
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
                print(f"Bureau result found: {burresult}")
                continue
            print("No bureau results found, proceeding to web search.")
            
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
            print(f"Total time for document: {webend - start:.4f} seconds")
            for i, url in enumerate(webresult[:3], start=1):
                if url[1] == None:
                    print(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
                else:
                    print(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
        except Exception as e:
            print("An error occurred during the search flow:", e)
            continue
    return

# Nested list from batching program
real_input = convert_file("testcsv/custtest.csv")
testFlow(real_input)