import os
from openai import OpenAI

# It's best practice to use an environment variable for your API key
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
client = OpenAI(api_key="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") 
#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
#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

# Define the research task with a system message and a user query
system_message = """
You are a tool created to help climate change researchers locate and download primary census data of all countries in the world.
You do not have to provide any analysis or summaries of the data, just return the raw data files.
Do:
- Web search to find all of the available years of census data for each country
- For each of these data files you find, provide the direct download link to the pdf document
  It will be almost impossible to be unable to find the documents as they are all publications by the government
  Prioritise documents sourced from official government websites, followed by libraries.
  Prioritise documents in pdf format, if unable to find a pdf, then provide a link to the webpage where the data can be found.
  In cases where the pdf document is not available, provide a link to the webpage where the data can be found.
- Return the metadata of each of the source websites that you download documents from or provide a link to.
- In the case where you can't find some specific census data, it's a good idea to search for the country name followed by "census data" or "population statistics" in the official language of the country.

Do not try to read the data in any way, just return the download links to the documents and the metadata.
In the case of countries that don't have publicly available census data, return the country's name and that it cannot be found as well as the search queries used.

The final output should be basically a dot point list with country name as headings, under which each link is given with notes on the country, year, specific province and any other metadata recorded.
"""

user_query = "Give me the download links to all the census data of Africa including all time periods"

response = client.responses.create(
    model="o4-mini-deep-research",
    input=[
        {"role": "system", "content": [{"type": "input_text", "text": system_message}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_query}]}
    ],
    background=True,
    tools=[{"type": "web_search_preview"}],
)

#print(response)

with open("response_output_all.txt", "w", encoding="utf-8") as f:
    f.write(str(response))
