import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_evidence(claim: str, search_results: list) -> dict:

    evidence_text = ""
    for i, result in enumerate(search_results):
        evidence_text += f"""
Source {i+1}:
Title: {result['title']}
URL: {result['url']}
Snippet: {result['snippet']}
Content: {result['page_text'][:1000]}
---
"""

    prompt = f"""
You are a fact-checking assistant.

The claim being verified is:
"{claim}"

Here are the web search results found to verify this claim:

{evidence_text}

Do the following:
1. Read all the sources carefully.
2. Summarize what the sources collectively say about this claim.
3. Note which sources support the claim, which contradict it, and which are neutral.
4. Highlight any important facts, dates, or figures found in the sources.

Respond in this exact format:
SUMMARY: <2 to 3 sentence summary of what sources say>
SUPPORTING: <list of source numbers that support the claim, or "None">
CONTRADICTING: <list of source numbers that contradict the claim, or "None">
KEY FACTS: <important facts found in sources>
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    output = response.text.strip()

    summary = ""
    supporting = ""
    contradicting = ""
    key_facts = ""

    for line in output.split("\n"):
        if line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
        elif line.startswith("SUPPORTING:"):
            supporting = line.replace("SUPPORTING:", "").strip()
        elif line.startswith("CONTRADICTING:"):
            contradicting = line.replace("CONTRADICTING:", "").strip()
        elif line.startswith("KEY FACTS:"):
            key_facts = line.replace("KEY FACTS:", "").strip()

    return {
        "summary": summary,
        "supporting": supporting,
        "contradicting": contradicting,
        "key_facts": key_facts
    }
