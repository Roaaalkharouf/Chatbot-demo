import requests
from bs4 import BeautifulSoup
import json

URLS = [
   " https://www.cirrusgo.com/about-us",
    "https://cirrusgo.com",
    "https://www.cirrusgo.com",
    "https://www.cirrusgo.com/our-services",
    "https://www.cirrusgo.com/event/data-ml-ai-roadshow-2025-11/page/introduction-aws-cloud-day-4",
    "https://www.cirrusgo.com/blog",
    "https://www.cirrusgo.com/aws"
]

content = {}

for url in URLS:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted elements
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    content[url] = text

# Save to JSON
with open("cirrusgo_content.json", "w") as f:
    json.dump(content, f, indent=2)
