import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Google Programmable Search Engine creds
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

# --- Tool definition (protos version) ---
tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="google_search",
            description="Perform a Google Custom Search and return PDF links.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "query": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="Search query to run"
                    )
                },
                required=["query"]
            )
        )
    ]
)

# Model setup (tools are bound to the model)
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction=(
        "You are a tool created to help climate change researchers locate primary "
        "population census data from the internet. Follow this order of actions: "
        "Preliminary step is to check the language of the user given info and correct the missing special characters before searching."
        "1) Use all user info to do a google search with the tool; add 'pdf' to the query. Do not use quotation marks as it limits results."
        "2) Note down the first 3 links returned. "
        "3) Using different grammar but same info, do another search and note 3 links. Can use local language for better range."
        "4) Repeat until you have 10 links. "
        "5) Return the link ordered by number of duplicates."
        "6) Document your search process in markdown."
    ),
    tools=[tool],
)

def run_search(query: str, max_calls: int = 5):
    """
    Runs a tool-calling loop correctly:
      user turn -> model function_call -> function_response -> model ...
    Ensures the function_response is the very next turn after function_call.
    """

    # Build history and make the first call
    history = [
        genai.protos.Content(
            role="user",
            parts=[genai.protos.Part(text=query)]
        )
    ]

    response = model.generate_content(history)

    all_links = []
    calls = 0

    while calls < max_calls:
        # Find a function_call in the model response (if any)
        fn_call = None
        for part in response.candidates[0].content.parts:
            if part.function_call:
                fn_call = part.function_call
                break

        if not fn_call:
            # No function call -> model has produced final text
            break

        calls += 1

        # Extract the query the model wants us to run
        search_query = fn_call.args.get("query", "")
        print(f"[Gemini requested search]: {search_query}")

        # ---- Perform the real Google CSE call ----
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": GOOGLE_API_KEY,
                "cx": SEARCH_ENGINE_ID,
                "q": search_query,
                "fileType": "pdf",   # bias towards PDFs
                "num": 10            # up to 10 results per call
            }
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            links = [item["link"] for item in data.get("items", [])]
        except Exception as e:
            print(f"[CSE ERROR]: {e}")
            links = []

        batch = links[:5]
        all_links.extend(batch)

        # ---- Append the model's function_call turn to history ----
        history.append(
            genai.protos.Content(
                role="model",
                parts=[genai.protos.Part(function_call=fn_call)]
            )
        )

        # ---- Append our function_response turn immediately after ----
        tool_response = genai.protos.FunctionResponse(
            name="google_search",
            # Send a real object; don't JSON-stringify unless you want to
            response={"links": batch}
        )
        history.append(
            genai.protos.Content(
                role="function",
                parts=[genai.protos.Part(function_response=tool_response)]
            )
        )

        # ---- Ask the model to continue with the updated history ----
        response = model.generate_content(history)

    return all_links, response.text

# -------------------
# Example run
# -------------------
user_query = "REPORT ON THE 1973 CENSUS OF POPULATION, Volume 1, Gilbert and Ellice Islands"

links, summary = run_search(user_query)

print("\n--- LINKS FOUND ---")
for i, link in enumerate(links, 1):
    print(f"{i}. {link}")

print("\n--- GEMINI SUMMARY WRITTEN TO FILE ---")
with open("response_output_text_geminisummary.md", "w", encoding="utf-8") as f:
    f.write(summary)
