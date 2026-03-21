from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
from dotenv import load_dotenv

from pipeline.step1_optimizer import optimize
from pipeline.step2_keyterms import extract_keyterms
from pipeline.step3_search import search_web
from pipeline.step4_summarize import summarize_evidence
from pipeline.step5_verdict import give_verdict

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "Fact Checker API is running"}

@app.post("/api/check")
def check_fact(news: NewsInput):
    try:
        step1 = optimize(news.text)
        claim = step1["claim"]
        translated = step1["translated"]
        time.sleep(10)

        step2 = extract_keyterms(claim)
        queries = step2["queries"]
        keyterms = step2["keyterms"]
        context = step2["context"]
        time.sleep(10)

        step3 = search_web(queries)
        time.sleep(10)

        step4 = summarize_evidence(claim, step3)
        time.sleep(10)

        step5 = give_verdict(claim, step4, step3)

        return {
            "claim": claim,
            "translated": translated,
            "keyterms": keyterms,
            "context": context,
            "verdict": step5["verdict"],
            "confidence": step5["confidence"],
            "explanation": step5["explanation"],
            "sources": step5["sources"]
        }

    except Exception as e:
        return {
            "error": str(e),
            "verdict": "Unverified",
            "confidence": 0,
            "explanation": "Something went wrong while processing.",
            "sources": []
        }
