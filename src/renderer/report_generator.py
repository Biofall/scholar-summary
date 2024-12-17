# src/renderer/report_generator.py

import datetime
import os

def generate_summary_report(summary: str, articles: list, output_dir: str = "reports", filename_prefix: str = None) -> str:
    """
    Generate a Markdown report with the summary and list of articles with citations,
    saving each report with a unique timestamp in the filename within the specified reports directory.

    Args:
        summary (str): The summarized text.
        articles (list): List of article dictionaries.
        output_dir (str): Directory to save the summary report (default is 'reports').
        filename_prefix (str): Optional prefix to include in the filename, before the timestamp.

    Returns:
        str: Path to the generated report.
    """
    # Generate a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if filename_prefix:
        filename = f"{filename_prefix}_summary_report_{timestamp}.md"
    else:
        filename = f"summary_report_{timestamp}.md"

    output_path = os.path.join(output_dir, filename)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Summary of Google Scholar Alerts\n\n")
        f.write(summary + "\n\n")
        f.write("## References\n")
        for i, article in enumerate(articles, start=1):
            title = article.get("title", "No Title")
            authors = ", ".join(article.get("authors", [])) if article.get("authors") else "Unknown authors"
            source = article.get("source", "Unknown source")
            doi = article.get("doi", "")
            link = article.get("link", "")

            # Include the title right after the article number
            citation = f"**Article {i}:** *{title}* by {authors}. _{source}_."
            if doi:
                citation += f" DOI: {doi}."
            if link:
                citation += f" [Link]({link})."
            f.write(f"- {citation}\n")

    return output_path