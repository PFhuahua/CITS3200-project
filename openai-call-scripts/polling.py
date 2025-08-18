import os
from dotenv import load_dotenv
import time
from openai import OpenAI

load_dotenv()

# It's best practice to use an environment variable for your API key
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
# Assuming you have the client object and the response ID
response_id = 'N/A'

# The `responses.poll` method is a simplified way to do this
# Note: The specific method name may vary depending on the most recent SDK
while True:
    response = client.responses.get(response_id)
    print(f"Current status: {response.status}")
    if response.status == 'completed':
        # Process the final output here
        with open("response_output_complete.txt", "w", encoding="utf-8") as f:
            f.write(str(response.output))
        print("Research completed!")
        break
    elif response.status in ['failed', 'canceled']:
        print("Research failed or was canceled.")
        break
    time.sleep(10) # Wait 10 seconds before polling again