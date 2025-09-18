from AITool import generate_search_queries, generate_lib_queries, rank_web_results
from Func_PDF_GoogleWS import PDF_Google_WS, LIB_Google_WS
from dotenv import load_dotenv
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

# Nested list from batching program
inputList = [["Name","Title (In English)","Original title","Country","Province","Date/Year of census","Date/Year of publication","Publisher","Volume number","File size of pdf original file  (KB)","Number of Pages of Table","Number of pages of original file"],
            ['cargx_18690101_0001_76319','The First Cenus of the Argentine Republic verified on the days of September 15th, 16th, and 17th, 1869','PRIMER CENSO DE LA REPUBLICA ARGENTINA VERIFICADO EN LOS DIAS 15, 16 y 17 de Setiembre de 1869','Argentina,National Record','September 15th, 16th, and 17th, 1869','1872','Diego G. de la Fuente - Superintendent of the Census','First entry','69960','N/A','806'],
            ['cargx_18950101_0001_76320','The Second Census of the Argentine Republic - Volume III - 1895 ','SEGUNDO  CENSO DE LA REPUBLICA ARGENTINA TOMO III Y ULTIMO 1895','Argentina','National Record','1895','1898','Diego G. de la Fuente - Superintendent of the Census','Volume 3','124085','N/A','784'],
            ['cargx_19140101_0001_76321','Third National Census - Taken on June 1st 1914',"TERCER CENSO NACIONAL - Levantado el 1' de Junio de 1914",'Argentina','National Record','1st of June 1914','1916','Dr. Victorino de la Plaza - National Comission','Volume 2','51029','N/A','587'],
            ['cargx_19470101_0002_76077','The 4th General Census of the Nation, 1947 - General Results of the Population Census','IV CENSO GENERAL DE LA NACION , 1947 - RESULTADOS GENERALES DEL CENSO DE POBLACION','Argentina','National Record','1947','1951','Ministry of Technical Affairs','Report 1','7043','N/A','42'],
            ['cargx_19470101_0001_76076','The 4th General Census of the Nation, 1947 - General Results of the Housing Census','IV CENSO GENERAL DE LA NACION , 1947 - RESULTADOS GENERALES DEL CENSO DE VIVIENDA','Argentina','National Record','1947','1951','Ministry of Technical Affairs','Report 2','7044','N/A','42'],
            ['cargx_19470101_0003_76078','The 4th General Census of the Nation, 1947 - General Results of the Agricultural and Livestock Census','IV CENSO GENERAL DE LA NACION , 1947 - RESULTADOS GENERALES DEL CENSO AGROPECUARIO','Argentina','National Record','1947','1951','Ministry of Technical Affairs','Report 3','7045','N/A','42'],
            ['cargx_19600101_0001_76079','The 5th National Population, Housing, and Agricultural Census - Volume I','V CENSO NACIONAL DE POBLACION, VIVIENDA Y AGROPECUARIO - TOMO I','Argentina','National Record','1960','1964','National Institute of Statistics and Censuses (INDEC)','Volume 1','5000','N/A','380'],
            ['cargx_19600101_0002_76080','The 5th National Population, Housing, and Agricultural Census - Volume II','V CENSO NACIONAL DE POBLACION, VIVIENDA Y AGROPECUARIO - TOMO II','Argentina','National Record','1960','1964','National Institute of Statistics and Censuses (INDEC)','Volume 2','5001','N/A','412'],
            ['cargx_19700101_0001_76081','The 6th National Population, Housing, and Agricultural Census - Volume I','VI CENSO NACIONAL DE POBLACION, VIVIENDA Y AGROPECUARIO - TOMO I','Argentina','National Record','1970','1973','National Institute of Statistics and Censuses (INDEC)','Volume 1','5002','N/A','400'],
            ['cargx_19700101_0002_76082','The 6th National Population, Housing, and Agricultural Census - Volume II','VI CENSO NACIONAL DE POBLACION, VIVIENDA Y AGROPECUARIO - TOMO II','Argentina','National Record','1970','1973','National Institute of Statistics and Censuses (INDEC)','Volume 2','5003','N/A','405'],
            ['cargx_19800101_0001_76083','The 7th National Population and Housing Census','VII CENSO NACIONAL DE POBLACION Y VIVIENDA','Argentina','National Record','1980','1982','National Institute of Statistics and Censuses (INDEC)','Volume 1','5004','N/A','350'],
            ['cargx_19910101_0001_76084','The 8th National Population and Housing Census','VIII CENSO NACIONAL DE POBLACION Y VIVIENDA','Argentina','National Record','1991','1993','Volume 1','5005','N/A','300'],
            ['cargx_20010101_0001_76085','The 9th National Population, Housing, and Household Census','IX CENSO NACIONAL DE POBLACION, HOGARES Y VIVIENDAS','Argentina','National Record','2001','2003','National Institute of Statistics and Censuses (INDEC)','Volume 1','5006','N/A','250']]
headerList = inputList[0]
for l in inputList[1:]:
    docInfo = {}
    for i, item in enumerate(l):
        docInfo[headerList[i]] = item
    start = time.time()
    print("Starting search...")
    iResult = testRunWS(docInfo)
    #print(iResult)
    with open("search_results.txt", "a", encoding="utf-8") as file:
        file.write(f"\nResults for document: {docInfo.get('Name', 'Unknown')}\n\n")
        try:
            ranked_results = json.loads(iResult)
        except json.JSONDecodeError as e:
            print("JSON decode error in iResult:", e)
            print(str(iResult))
            continue
        for i, url in enumerate(ranked_results, start=1):
            if url[1] == None:
                file.write(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
            else:
                file.write(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")
    print(f"Results for document: {docInfo.get('Name', 'Unknown')} written to search_results.txt")
    end = time.time()
    print(f"Process time: {end - start:.4f} seconds")
    time.sleep(2)
    '''d = input("\nPress l if you want to search library instead, any other key to continue: ")
    if d.lower() == "l":
        print("Not implemented yet")'''
