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
    """Save the list of articles to the single JSON file."""
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

    # Add a timestamp field to each newly added article
    # Format: "YYYY-MM-DD HH:MM:SS"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for article in articles_to_add:
        article["added_timestamp"] = now_str

    if articles_to_add:
        updated_articles = existing_articles + articles_to_add
        save_articles(updated_articles)

    return articles_to_add

def get_all_articles() -> List[Dict]:
    """Return all currently stored articles."""
    return load_articles()