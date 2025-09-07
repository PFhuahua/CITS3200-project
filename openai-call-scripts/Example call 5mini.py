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
User provides info including title, location, and year of the document.
You will search the web for a pdf of the document and return the direct download link.
You must return only a direct 100% match.
If you cannot find a direct link, return "Could not find".
For testing purposes, document your search process in md format.
"""

user_query = "title: Alphabetical Index Of Occupations and Industries, location: United States, year: 1950"

response = client.responses.create(
    model="gpt-5-mini-2025-08-07",
    input=[
        {"role": "system", "content": [{"type": "input_text", "text": system_message}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_query}]}
    ],
    background=True,
    tools=[{"type": "web_search_preview"}],
    max_output_tokens=100000,
    reasoning={"effort": "low"},
    text={"verbosity": "low"}
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
        #with open("response_output_complete_5mini.md", "w", encoding="utf-8") as f:
            #f.write(str(response.output))
        # Extract and save the markdown text
        for item in response.output:
            if hasattr(item, "content") and item.content is not None:
                for content_item in item.content:
                    if hasattr(content_item, "text"):
                        #with open("response_output_text_web.md", "w", encoding="utf-8") as f:
                            #f.write(content_item.text)
                        print(content_item.text)
                        break
        break
    elif response.status in ['failed', 'canceled']:
        print("Research failed or was canceled.")
        break
    time.sleep(10) # Wait 10 seconds before polling again
