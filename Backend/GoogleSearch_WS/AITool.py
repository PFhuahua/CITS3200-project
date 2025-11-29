import google.generativeai as genai
import time
import re

def generate_all_queries(DocInfo, max_retries=3, delay=2):
    prompt = (
        f"Document info given: {DocInfo}\n"
        "Generate optimized search queries based on the above information."
    )
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are a search query optimiser."
            "The context is that a user is searching for census data from some given country and year."
            "You will be provided some of the folowing: the name of the document, the country, the province, the year of the census, year of publication, publisher, volume number and more."
            "With these info, you will generate multiple search queries for different cases:"
            "1. A search query that will be best fit for finding a match in big libraries."
            "   The query should be made up of the exact title primarily"
            "   Next check if the year of the census and the country are in the title, if not add them to the query."
            "   Make sure to fix any typos and accents/special characters in the title."
            "   Do not use double quotes for perfect matches, they're not needed for libs."
            "   Be as concise as you can. Unless the title is very generic do not add any other fields to the query. In fact you will want to remove the tome/volume if they're included in the query."
            "   After that, depending on colonisation status at the time of the census, use either French, Spanish or Portugese and provide a query with the same restrictions in that language too."
            "2. A search query that will be best fit for finding a match in local statistics bureaus."
            "   Include at least the title and year for the best results. These 2 fields must be in the query for it to have any chance of finding the correct thing UNLESS the title includes the year already."
            "   Use common sense to decide whether or not to add extra fields. Eg. if there is already a year in the title then don't make it confusing by adding another year."
            "   Make sure to fix any typos and accents/special characters in the title."
            "   Do not use double quotes for perfect matches, they're not needed for bureaus."
            "   After that, depending on the country of origin for the document, generate the same query but in that language."
            "3. A search query that will be best fit for finding a match on google. Do not use double quotes for perfect matches."
            "   Not all of the data is necesary for the search, use your best judgement to decide what to include and what to exclude."
            "   You can include pdf in the query but do not force pdf filetype as it restricts the results."
            "   After that, depending on colonisation status at the time of the census, use either French, Spanish or Portugese and provide a query in that language too."
            "Do not include any explanation or formatting outside the JSON. DO NOT USE TRIPLE QUOTES FOR CODE SNIPPETS."
            'Return a nested list of each two queries as a JSON array of strings, e.g. [["Query 1", "Query 2"],["Query 3", "Query 4"]] IN PLAIN TEXT WITH NO CODE CHUNK.'
        ),
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

def rank_web_results(Query, ResInfo, max_retries=3, delay=2):
    prompt = (
        f"Search results given: {ResInfo}\n"
        f"Original query: {Query}\n"

    )
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
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

def match_result(Queries, ResInfo, max_retries=3, delay=2):
    prompt = (
        f"Search results given: {ResInfo}\n"
        f"Original query: {Queries}\n"

    )
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=(
        "You are a search result matching system. You will be given a dict with metadata of the doc being searched and a dictionary with the library name as key and a list of search results as values."
        "The search results will be in the format: {lib_name: [[URL,contents],[URL2,contents2]]}."
        "**IMPORTANT PRIORITY**First scan all of the text given for each result for keywords including 'microform', 'microfilm', types like 'book' and codes like 'FILM 123' and immediately disqualify them no matter how good they are. Completely drop the disqualified results, forget them completely."
        "After that, looking at all the dict metadata, see if any of the result titles and snippets match the document being searched. Remove any results that are irrelevant. Note we are looking for data not preview or summaries unless specified in the doc info."
        "Choose the single URL out of the eligible options with the contents that matches the doc being searched the best."
        "Prioritise exact matches of the name of the census, year of the census, publisher and volume number over the content summary of documents."
        "If there are no matches, return an empty JSON array."
        "Return the best result as a JSON array, where the array contains [lib_name, URL, File name, Very brief summary of contents]."
        "Do not include any explanation or formatting outside the JSON. DO NOT USE TRIPLE QUOTES FOR CODE SNIPPETS."
        )
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            proc_text = response.text.strip().replace('```json', '').replace('`', '')
            return re.sub(r'\\([^"\\/bfnrtu])', r'\\\\\1', proc_text)
        except Exception as e:
            print("Exception caught in match_result:", repr(e), type(e), flush=True)
            if "503" in str(e):
                print(f"503 Service Unavailable. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})", flush=True)
                time.sleep(delay)
            else:
                print("Error generating search queries:", e, flush=True)
                break
    return '[""]'