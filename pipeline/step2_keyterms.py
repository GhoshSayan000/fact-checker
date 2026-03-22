_______________________________________________________________________________________________________________________________________________________________________________
#Step 2: Extracts key terms,context and generates search queries from the claim.
# These queries are used to search the web for verification evidence.
_______________________________________________________________________________________________________________________________________________________________________________
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_keyterms(claim: str) -> dict:
    prompt = f"""
You are a fact-checking assistant.

Given this factual claim:
"{claim}"

Do the following:
1. Extract the key terms (important words and phrases) from the claim.
2. Identify the context (what topic or domain this claim is about).
3. Generate 2 to 3 specific search queries that can be used to verify this claim on the web.

Respond in this exact format:
KEYTERMS: <comma separated key terms>
CONTEXT: <one sentence describing the topic>
QUERIES:
- <search query 1>
- <search query 2>
- <search query 3>
"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    output = response.text.strip()

    keyterms = ""
    context = ""
    queries = []

    lines = output.split("\n")
    reading_queries = False

    for line in lines:
        if line.startswith("KEYTERMS:"):
            keyterms = line.replace("KEYTERMS:", "").strip()
        elif line.startswith("CONTEXT:"):
            context = line.replace("CONTEXT:", "").strip()
        elif line.startswith("QUERIES:"):
            reading_queries = True
        elif reading_queries and line.strip().startswith("-"):
            queries.append(line.strip().lstrip("-").strip())

    return {
        "keyterms": keyterms,
        "context": context,
        "queries": queries
    }
