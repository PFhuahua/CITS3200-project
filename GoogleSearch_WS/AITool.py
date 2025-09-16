import google.generativeai as genai

def generate_search_queries(DocInfo):
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
            "Return the two queries in the following format: 'Query 1; Query 2' DO NOT FORMAT FOR MARKDOWN WITH TRIPLE QUOTES."
        ),
    )

    response = model.generate_content(prompt)
    return response.text.strip()

def generate_lib_queries(DocInfo):
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
            "Return the two queries in the following format: 'Query 1; Query 2' DO NOT FORMAT FOR MARKDOWN WITH TRIPLE QUOTES."
        ),
    )

    response = model.generate_content(prompt)
    return response.text.strip()

def rank_web_results(Query, ResInfo):
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
        "Return the ranking as a string of tuples in the format of: '(URL, file size, title, snippet); (URL1, file size1, title1, snippet1)'."
        "Make sure every open bracket has a close bracket."
        "DO NOT FORMAT FOR MARKDOWN WITH TRIPLE QUOTES."
        )
    )

    response = model.generate_content(prompt)
    return response.text.strip()