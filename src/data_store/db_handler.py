# src/data_store/db_handler.py

import json
import os
from typing import List, Dict
from datetime import datetime

DATA_DIR = "data"
DATA_FILE_PATH = os.path.join(DATA_DIR, "articles.json")

def load_articles() -> List[Dict]:
    """Load existing articles from the JSON file. If the file does not exist, return an empty list."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.isfile(DATA_FILE_PATH):
        return []
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []

def save_articles(articles: List[Dict]) -> None:
    """Save the list of articles to the main JSON file."""
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def store_articles(new_articles: List[Dict]) -> List[Dict]:
    """
    Store articles in the JSON file, skipping duplicates by link.
    Returns the list of newly added articles.
    """
    existing_articles = load_articles()
    existing_links = {article["link"] for article in existing_articles if "link" in article}

    # Filter out duplicates
    articles_to_add = [a for a in new_articles if a.get("link") and a["link"] not in existing_links]

    if articles_to_add:
        updated_articles = existing_articles + articles_to_add
        # Save to the main file
        save_articles(updated_articles)

        # Also create a timestamped snapshot to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(DATA_DIR, f"articles_{timestamp}.json")
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(updated_articles, f, ensure_ascii=False, indent=2)

    return articles_to_add