import time
from openai import OpenAI

# It's best practice to use an environment variable for your API key
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") 
client = OpenAI(api_key="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") 

# Assuming you have the client object and the response ID
response_id = 'resp_68a1ed670b7081a08ba4ea39353ae5430bf90dfa0fa23e04'

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