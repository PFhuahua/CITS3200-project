from AITool import generate_search_queries, generate_lib_queries, rank_web_results
import time
import ast

def testPrompts():
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
        #print(docInfo)
        webresponse = generate_search_queries(docInfo).split(";")
        libresponse = generate_lib_queries(docInfo).split(";")
    return webresponse, libresponse

def testWebRank(Query):
    # Input from web search results
    inputList = [('https://ravignanidigital.com.ar/_bol_ravig/n16_17/n1617a05.pdf', None, 'Estadística censal y construcción de la Nación : el caso argentino ...', '... censos nacionales de po- blación fueron Diego G. De la Fuente (superintendente del Primer Censo Nacional, director del Cen- so de la Provincia de Buenos\xa0...'),
                ('http://sedici.unlp.edu.ar/bitstream/handle/10915/11616/Documento_completo__.pdf?sequence=1&isAllowed=y', 1997547, 'HISTORIA Y RESULTADOS DEL CENSO CONFEDERAL DE 1857 ...', '(1) DIEGO DE LA FUENTE. Primer Censo de Ja República Argentina verificado en los días 15, 16 y 17 de setiembre de 1869 baio la direcci6n de.,. Bs. As., 1872\xa0...'),
                ('https://www.estadistica.ec.gba.gov.ar/dpe/Estadistica/censos/C1895-T2.pdf', None, 'Segundo Censo de la Nación Argentina - MAYO 1895', 'Personal que ha cooperado à la realización del censo. PRIMERA PARTE. CONSIDERACIONES SOBRE LOS RESULTADOS DEL CENSO. NACIONAL ARGENTINO, POR. Gabriel CarRASCO\xa0...'),
                ('http://www.estadistica.ec.gba.gov.ar/dpe/Estadistica/censos/C1869-TU.pdf', None, 'El primer censo en 1869', 'REPUBLICA ARGENTINA. VERIFICADO EN LOS DIAS γ. CENSOS. 15, 16 y 17 de Setiembre de 1869. Bujo la direccion de Diego G. de la Fuente. SUPERINTENDENTE DEL CENSO.'),
                ('https://adeh.org/wp-content/uploads/2023/07/ADEH-2022-II_5_quienes-y-cuantos.pdf', 3130205, '¿Quiénes y cuántos? La población indígena del norte y oeste de ...', 'a través del primer censo nacional de Argentina (1869). ... DE LA FUENTE, Diego (1872): “Introducción”, en Primer Censo de la República Argentina.')]
    webrank = rank_web_results(Query, inputList)
    return webrank

start = time.time()

webres, libres = testPrompts()
print("Web queries:", webres)
print("Lib queries:", libres, "\n")
mid = time.time()
print(f"Prompt generation time: {mid - start:.4f} seconds\n")

webrank = testWebRank(webres[0]).split(";")
'''for i in webrank:
    print(ast.literal_eval(i.strip())[1])
'''
for i, url in enumerate(webrank, start=1):
    url = ast.literal_eval(url.strip())
    if url[1] == None: print(f"{i}. {url[0]} \nfile size: UNKNOWN.\nTitle: {url[2]}, \nsnippet: {url[3]}\n")
    else: print(f"{i}. {url[0]}, \nfile size: {round(int(url[1])/1000,0)} KB.\n Title: {url[2]}, \nsnippet: {url[3]}\n")

end = time.time()
print(f"Ranking time: {end - start:.4f} seconds")