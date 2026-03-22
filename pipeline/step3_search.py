______________________________________________________________________________________________________________________________________________________________________________
#Step 3: Searches the web using SerpAPI and scrapes page content.
# It returns a list of results with title ,URL,snippet and page text.
______________________________________________________________________________________________________________________________________________________________________________
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_web(queries: list) -> list:
    all_results = []

    for query in queries:
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 3,
            "engine": "google"
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        organic_results = data.get("organic_results", [])

        for result in organic_results[:3]:
            title = result.get("title", "")
            link = result.get("link", "")
            snippet = result.get("snippet", "")

            page_text = scrape_page(link)

            all_results.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "page_text": page_text[:2000]
            })

    return all_results


def scrape_page(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]

    except Exception:
        return ""
