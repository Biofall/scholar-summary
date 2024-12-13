# src/email_client/email_parser.py

from bs4 import BeautifulSoup
import re
import urllib.parse

def clean_title_line(title_line: str) -> str:
    # Remove leading [PDF], [HTML], etc.
    cleaned = re.sub(r"^\[.*?\]\s*", "", title_line, flags=re.IGNORECASE).strip()
    return cleaned

def extract_actual_link(redirect_url: str) -> str:
    """
    Extract the actual article URL from the Google Scholar redirect URL.
    """
    parsed = urllib.parse.urlparse(redirect_url)
    qs = urllib.parse.parse_qs(parsed.query)
    # 'url' parameter usually holds the actual article link
    if 'url' in qs:
        return qs['url'][0]
    return redirect_url

def parse_scholar_alert(raw_email_html: str):
    """
    Parse a Google Scholar alert HTML to extract articles.

    Returns:
        List of article dicts:
        {
          "title": str,
          "link": str,
          "snippet": str,
          "source": str,
          "authors": list[str],
          "publication_date": ""
        }
    """
    soup = BeautifulSoup(raw_email_html, "html.parser")
    articles = []
    
    # Each article block starts with an <h3> that contains <a class="gse_alrt_title">
    title_blocks = soup.find_all("h3", text=False)
    # Filter only those h3s that contain a title link
    for h3 in title_blocks:
        title_a = h3.find("a", class_="gse_alrt_title")
        if not title_a:
            continue  # Not an article title block
        
        # Extract title
        raw_title = title_a.get_text(strip=True)
        title = clean_title_line(raw_title)

        # Extract link (Scholar redirect)
        redirect_url = title_a.get("href", "")
        link = extract_actual_link(redirect_url)

        # The next element(s) after h3:
        # - The authors/source div is right after the h3 (possibly with a <br> or newline)
        authors_source_div = h3.find_next("div", style=re.compile("color:#006621"))
        authors_line = authors_source_div.get_text(strip=True) if authors_source_div else ""
        print("authors_line:", repr(authors_line))

        # Parse authors and source
        authors = []
        source = ""

        if '- ' in authors_line:
            authors_part, source_part = authors_line.split('- ', 1)
            # authors separated by commas
            authors = [a.strip() for a in authors_part.split(',') if a.strip()]

            # Remove trailing ", year" if present
            print("Before cleaning source_part:", repr(source_part))
            source_part = re.sub(r',\s*\d{4}$', '', source_part).strip()
            print("After cleaning source_part:", repr(source_part))
            source = source_part
        else:
            # If no ' - ', treat the entire line as source
            source = authors_line.strip()

        # Next, the snippet line:
        snippet_div = authors_source_div.find_next("div", class_="gse_alrt_sni") if authors_source_div else None
        snippet = snippet_div.get_text(" ", strip=True) if snippet_div else ""

        article = {
            "title": title,
            "link": link,
            "snippet": snippet,
            "source": source,
            "authors": authors,
            "publication_date": ""
        }

        articles.append(article)

    return articles