import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def give_verdict(claim: str, evidence: dict, search_results: list) -> dict:

    sources_list = ""
    for i, result in enumerate(search_results):
        sources_list += f"Source {i+1}: {result['url']}\n"

    prompt = f"""
You are an expert fact-checker.

The claim being verified is:
"{claim}"

Here is the summarized evidence from web sources:

Summary: {evidence['summary']}
Supporting sources: {evidence['supporting']}
Contradicting sources: {evidence['contradicting']}
Key facts found: {evidence['key_facts']}

Sources checked:
{sources_list}

Based on all this evidence, give a final fact-check verdict.

Respond in this exact format:
VERDICT: <True or False or Unverified>
CONFIDENCE: <a number between 0 and 100 representing how confident you are>
EXPLANATION: <2 to 3 sentences explaining why you gave this verdict>
SOURCES: <comma separated list of URLs that were most useful>
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    output = response.text.strip()

    verdict = "Unverified"
    confidence = 0
    explanation = ""
    sources = []

    for line in output.split("\n"):
        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                confidence = int(line.replace("CONFIDENCE:", "").strip())
            except:
                confidence = 0
        elif line.startswith("EXPLANATION:"):
            explanation = line.replace("EXPLANATION:", "").strip()
        elif line.startswith("SOURCES:"):
            sources_raw = line.replace("SOURCES:", "").strip()
            sources = [s.strip() for s in sources_raw.split(",")]

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "sources": sources
    }
