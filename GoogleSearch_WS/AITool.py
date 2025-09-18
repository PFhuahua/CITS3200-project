import google.generativeai as genai
import time
import re

def generate_search_queries(DocInfo, max_retries=3, delay=2):
    prompt = (
        f"Document info given: {DocInfo}\n"
        "Generate optimized search queries based on the above information."
    )
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are a web search query optimiser."
            "The context is that a user is searching for census data from some given country and year."
            "You will be provided some of the folowing: the name of the document, the country, the province, the year of the census, year of publication, publisher, volume number and more."
            "With these info, you will generate a search query that will be best fit for finding a match on google. Do not use double quotes for perfect matches."
            "Not all of the data is necesary for the search, use your best judgement to decide what to include and what to exclude."
            "You can include pdf in the query but do not force pdf filetype as it restricts the results."
            "After that, depending on colonisation status at the time of the census, use either French, Spanish or Portugese and provide a query in that language too."
            "Do not include any explanation or formatting outside the JSON. DO NOT USE TRIPLE QUOTES FOR CODE SNIPPETS."
            'Return the two queries as a JSON array of strings, e.g. ["Query 1", "Query 2"] IN PLAIN TEXT WITH NO CODE CHUNK.'
        ),
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "503" in str(e):
                print(f"503 Service Unavailable. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                print("Error generating search queries:", e)
                break
    return '[""]'

def generate_lib_queries(DocInfo, max_retries=3, delay=2):
    prompt = (
        f"Document info given: {DocInfo}\n"
        "Generate optimized search queries based on the above information."
    )
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are a library search query optimiser."
            "The context is that a user is searching for census data from some given country and year in an internal library search."
            "You will be provided some of the folowing: the name of the document, the country, the province, the year of the census, year of publication, publisher, volume number and more."
            "With these info, you will generate a search query that will be best fit for finding a match in big libraries."
            "Not all of the data is necesary for the search, use your best judgement to decide what to include and what to exclude."
            "After that, depending on colonisation status at the time of the census, use either French, Spanish or Portugese and provide a query in that language too."
            "Do not include any explanation or formatting outside the JSON. DO NOT USE TRIPLE QUOTES FOR CODE SNIPPETS"
            'Return the two queries as a JSON array of strings, e.g. ["Query 1", "Query 2"] IN PLAIN TEXT WITH NO CODE CHUNK.'
        ),
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "503" in str(e):
                print(f"503 Service Unavailable. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                print("Error generating search queries:", e)
                break
    return '[""]'

def rank_web_results(Query, ResInfo, max_retries=3, delay=2):
    prompt = (
        f"Search results given: {ResInfo}\n"
        f"Original query: {Query}\n"
        
    )
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        system_instruction=(
        "You are a web search result ranking system. You will be given a list of search results and the query string."
        "The search results will be in the format: (URL, file size in bytes or None if unknown, title, snippet)."
        "Rank the results by how well they match the query."
        "Do not include any explanation or formatting outside the JSON. DO NOT USE TRIPLE QUOTES FOR CODE SNIPPETS"
        "Return the ranking as a JSON array of arrays, where each array contains [URL, file size, title, snippet] IN PLAIN TEXT WITH NO CODE CHUNK."
        "I REPEAT NO BACKTICKS NO CODECHUNKS JUST THE RAW JSON TEXT."
        )
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            proc_text = response.text.strip().replace('```json', '').replace('`', '')
            return re.sub(r'\\([^"\\/bfnrtu])', r'\\\\\1', proc_text)
        except Exception as e:
            if "503" in str(e):
                print(f"503 Service Unavailable. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                print("Error generating search queries:", e)
                break
    return '[""]'