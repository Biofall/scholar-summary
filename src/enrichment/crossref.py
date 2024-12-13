import requests
import re
import html

CROSSREF_API_URL = "https://api.crossref.org/works"

def clean_title(title: str) -> str:
    """
    Remove leading markers like [PDF], [HTML], etc. from the title.
    Also strip leading/trailing whitespace.
    """
    # Common patterns: [PDF], [HTML], [Free], etc.
    # We'll remove anything in square brackets at the start of the title.
    cleaned = re.sub(r"^\[.*?\]\s*", "", title, flags=re.IGNORECASE).strip()
    return cleaned

def query_crossref_by_title(title: str, max_results=5):
    """
    Query the CrossRef API by title. Return up to max_results items.
    """
    params = {
        "query.title": title,
        "rows": max_results
    }
    response = requests.get(CROSSREF_API_URL, params=params, timeout=10)
    if response.status_code == 200:
        return response.json().get("message", {}).get("items", [])
    return []

def best_match_article(items, original_title):
    """
    Given a list of CrossRef items, pick the best match by comparing the title.
    We'll do a simple case-insensitive substring check or similarity check.
    """
    original_lower = original_title.lower()
    best_item = None
    best_score = 0.0

    for item in items:
        item_title = ""
        # CrossRef titles are often a list, take the first if available
        if "title" in item and isinstance(item["title"], list) and len(item["title"]) > 0:
            item_title = item["title"][0].lower()
        # Simple scoring: count how many words overlap, or length of substring match
        # For now, let's do a basic similarity measure: proportion of matching words
        original_words = set(original_lower.split())
        item_words = set(item_title.split())
        if not item_words:
            continue
        overlap = len(original_words.intersection(item_words)) / len(original_words)
        
        # Choose the item with the highest overlap
        if overlap > best_score:
            best_score = overlap
            best_item = item

    # We can also add a threshold if needed. For now, if best_score is too low (say < 0.2), 
    # we consider it no match.
    if best_score < 0.2:
        return None

    return best_item

def strip_html_tags(text: str) -> str:
    """Remove any HTML or JATS tags from the abstract."""
    # A simple approach: remove tags with a regex. For more complex parsing, 
    # we could use BeautifulSoup.
    stripped = re.sub(r"<[^>]+>", "", text)
    # Unescape HTML entities
    stripped = html.unescape(stripped)
    return stripped.strip()

def extract_authors(item):
    """Extract authors from a CrossRef item."""
    authors = []
    if "author" in item and isinstance(item["author"], list):
        for a in item["author"]:
            # CrossRef typically gives a structured author object with 'given' and 'family' names
            given = a.get("given", "")
            family = a.get("family", "")
            full_name = (given + " " + family).strip()
            if full_name:
                authors.append(full_name)
    return authors

def extract_publication_date(item):
    """
    Extract a publication date from the item. 
    CrossRef might have 'issued', 'published-print', or 'published-online'.
    We'll try them in order of preference.
    """
    date_fields = ["issued", "published-online", "published-print"]
    for field in date_fields:
        date_info = item.get(field, {})
        if "date-parts" in date_info and isinstance(date_info["date-parts"], list) and len(date_info["date-parts"]) > 0:
            parts = date_info["date-parts"][0]
            # Date-parts is usually [year, month, day]
            # We'll just join them with '-'. Missing parts default to 1 or empty.
            year = str(parts[0]) if len(parts) > 0 else "0000"
            month = str(parts[1]) if len(parts) > 1 else "01"
            day = str(parts[2]) if len(parts) > 2 else "01"
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return ""

def enrich_article_data(article):
    """
    Enrich the article data by querying CrossRef with its title.
    If a match is found, add DOI, full abstract, authors, and a standardized publication date.
    
    article: {
      "title": "...",
      "link": "...",
      "snippet": "...",
      "source": "...",
      "authors": [...],
      "publication_date": "..."
    }

    Returns the enriched article (possibly updated) or the original if no match found.
    """
    cleaned_title = clean_title(article.get("title", ""))
    if not cleaned_title:
        return article

    items = query_crossref_by_title(cleaned_title)
    if not items:
        # No results found
        return article

    best_item = best_match_article(items, cleaned_title)
    if not best_item:
        return article

    # If we have a best match, update fields
    if "DOI" in best_item:
        article["doi"] = best_item["DOI"]

    # Abstract
    if "abstract" in best_item and isinstance(best_item["abstract"], str):
        article["snippet"] = strip_html_tags(best_item["abstract"])

    # Authors
    # If we have authors, we might overwrite or just update if empty
    new_authors = extract_authors(best_item)
    if new_authors:
        article["authors"] = new_authors

    # Publication date
    pub_date = extract_publication_date(best_item)
    if pub_date:
        article["publication_date"] = pub_date

    # Source (journal)
    # CrossRef item often has "container-title" which is the journal name
    if "container-title" in best_item and len(best_item["container-title"]) > 0:
        article["source"] = best_item["container-title"][0]

    return article