import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
ARTICLE_PATH = "generated_article.md"

def publish_to_devto():
    if not DEVTO_API_KEY:
        print("Error: DEVTO_API_KEY not found in .env file.")
        return

    if not os.path.exists(ARTICLE_PATH):
        print(f"Error: Article file '{ARTICLE_PATH}' not found.")
        return

    with open(ARTICLE_PATH, "r") as f:
        content = f.read()

    # The markdown has frontmatter, Dev.to API prefers JSON metadata
    # But since the prompt requires frontmatter, we will pass it anyway, 
    # Dev.to usually parses it correctly if passed as `body_markdown`.
    
    headers = {
        "Content-Type": "application/json",
        "api-key": DEVTO_API_KEY
    }

    # Extract title from frontmatter
    lines = content.split('\n')
    title = "Building an Autonomous Data Pipeline Sentinel with Hierarchical Memory"
    tags = ["python", "ai", "architecture", "data"] # Max 4 tags (Lesson 4)

    payload = {
        "article": {
            "title": title,
            "body_markdown": content,
            "published": True,
            "tags": tags
        }
    }

    url = "https://dev.to/api/articles"
    print("Publishing to Dev.to...")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Successfully published! URL: {data.get('url')}")
    else:
        print(f"❌ Failed to publish. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    publish_to_devto()
