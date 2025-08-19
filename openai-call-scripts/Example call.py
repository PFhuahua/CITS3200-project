import os
from dotenv import load_dotenv
import time
from openai import OpenAI

load_dotenv()

# It's best practice to use an environment variable for your API key
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Define the research task with a system message and a user query
system_message = """
You are a tool created to help climate change researchers locate primary census data from some given country or location limitations.
The user will give you a prompt with specifications on which census they're looking for whether it's the country, year, province, title of the document or something else.
You are to search the web for census pdfs fitting the given constraints and return a link to the download location if you find it as well as the metadata of the website it's on.
Do not give a generic archive website where the user has to search for the data themselves.
You should return the link to the pdf file directly, or at the very least a direct link where the most the user needs to do is access it and click the immediately visible download link.
For instances where there are many pages in the website, find the page the document is on and make sure to include it in the link so the user doesnt need to look through the pages themselves.
You should return a list of links, each with notes on its country, year, province as well as other metadata.
DO NOT TRY TO LOOK INTO THE DATA, AT MOST LOOK AT THE TITLE.
If you are unable to find any pdfs of the census file, try searching in the native language.
If that doesn't return anything either, then simply return the given location/constraints and then note that nothing could be found.
"""

user_query = "Find me the data for Egypt between 2000 and 2020"

response = client.responses.create(
    model="o4-mini-deep-research-2025-06-26",
    input=[
        {"role": "system", "content": [{"type": "input_text", "text": system_message}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_query}]}
    ],
    background=True,
    tools=[{"type": "web_search_preview"}],
    max_output_tokens=100000, 
    max_tool_calls=15
)

print(response.id)
RESP_ID = response.id

# The `responses.poll` method is a simplified way to do this
# Note: The specific method name may vary depending on the most recent SDK
while True:
    response = client.responses.retrieve(RESP_ID)
    print(f"Current status: {response.status}")
    if response.status == 'completed':
        # Process the final output here
        with open("response_output_complete.md", "w", encoding="utf-8") as f:
            f.write(str(response.output))
        with open("response_output_text.md", "w", encoding="utf-8") as f:
            f.write(response.output.ResponseOutputMessage.content.ResponseOutputText.text)
        print("Research completed!")
        break
    elif response.status in ['failed', 'canceled']:
        print("Research failed or was canceled.")
        break
    time.sleep(10) # Wait 2 seconds before polling again
