import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document


def load_website(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    cleaned_text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    return [
        Document(
            page_content=cleaned_text,
            metadata={
                "source": url,
                "file_type": "website",
                "page": 0
            }
        )
    ]