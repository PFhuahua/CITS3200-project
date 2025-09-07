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
You are a tool created to help climate change researchers locate primary population census data from the internet, specifically by searching public libraries.
User query will include several parameters including location range and date range.
Your task is to search both the local libraries and the globally acclaimed libraries for the pdf (or a compressed file format like zip) version of the population census or the complete census for the specified locations and dates.
The target is either a population/migration census or a complete census (PRIORITY) with all the fields, do not return 3rd party stats or nonrelated stats.
Prioritise big and reputable libraries including but not limited to the British Library, the French National Library, the University of Texas Libraries and others like them.
The end result should be a list of non repeating publically accessible library urls of the documents, headered by location and date ranges.
DO NOT RETURN NUMERICAL DATA, YOU ARE ONLY LOOKING FOR DOCUMENTS FROM LIBRARIES.
"""

user_query = "Find me the 1851 census of ireland."

response = client.responses.create(
    model="o4-mini-deep-research-2025-06-26",
    input=[
        {"role": "system", "content": [{"type": "input_text", "text": system_message}]},
        {"role": "user", "content": [{"type": "input_text", "text": user_query}]}
    ],
    background=True,
    tools=[{"type": "web_search_preview"}],
    max_output_tokens=110000,
    max_tool_calls=20
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
        with open("response_output_complete_lib.md", "w", encoding="utf-8") as f:
            f.write(str(response.output))
        # Extract and save the markdown text
        for item in response.output:
            if hasattr(item, "content") and item.content is not None:
                for content_item in item.content:
                    if hasattr(content_item, "text"):
                        with open("response_output_text_lib.md", "w", encoding="utf-8") as f:
                            f.write(content_item.text)
                        print("Research completed! Markdown written.")
                        break
        break
    elif response.status in ['failed', 'canceled']:
        print("Research failed or was canceled.")
        break
    time.sleep(10) # Wait 10 seconds before polling again
