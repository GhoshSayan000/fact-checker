import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def optimize(text: str) -> dict:
    prompt = f"""
You are a fact-checking assistant.

Given the following news or social media post (possibly in Hindi, Tamil, Bengali, or any Indian language):

"{text}"

Do the following:
1. Detect the language and translate it to English if it is not already in English.
2. Remove all conversational filler, emojis, hashtags, and irrelevant content.
3. Extract ONLY the core factual claim as ONE clean, simple English sentence.

Respond in this exact format:
TRANSLATED: <full english translation>
CLAIM: <single core factual claim>
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    output = response.text.strip()

    translated = ""
    claim = ""

    for line in output.split("\n"):
        if line.startswith("TRANSLATED:"):
            translated = line.replace("TRANSLATED:", "").strip()
        elif line.startswith("CLAIM:"):
            claim = line.replace("CLAIM:", "").strip()

    return {
        "translated": translated,
        "claim": claim
    }
