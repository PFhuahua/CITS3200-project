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
You are a tool created to help climate change researchers locate primary population census data from the internet.
User query will include several parameters including location range and date range.
Your task is to search the web for the pdf version of the population census or the complete census for the specified locations and dates.
It does not have to be named a population census, return results that include any kind of data on population and migration.
If you find a suitable source, you will scrape the page and find the url of the pdf.
If there is no pdf download url on the webpage, return the url of the webpage instead, but only after scanning the entire page for links.
The end result should be a list of pdf download urls or webpage urls, broken up by location and date ranges given.
Most of the time you will need to crawl through both the official government records as well as major libraries to conclude that there are no more censuses conducted.
"""

user_query = "Find me the census data for Nigeria between 2000 and 2020"

response = client.responses.create(
    model="o4-mini-deep-research-2025-06-26",
    input=[
        {"role": "system", "content": [{"type": "input_text", "text": system_message}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_query}]}
    ],
    background=True,
    tools=[{"type": "web_search_preview"}],
    max_output_tokens=110000, 
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
        with open("response_output_complete_new.md", "w", encoding="utf-8") as f:
            f.write(str(response.output))
        # Extract and save the markdown text
        for item in response.output:
            if hasattr(item, "content") and item.content is not None:
                for content_item in item.content:
                    if hasattr(content_item, "text"):
                        with open("response_output_text.md", "w", encoding="utf-8") as f:
                            f.write(content_item.text)
                        print("Research completed! Markdown written.")
                        break
        break
    elif response.status in ['failed', 'canceled']:
        print("Research failed or was canceled.")
        break
    time.sleep(10) # Wait 2 seconds before polling again
