# src/renderer/report_generator.py

import datetime

def generate_summary_report(summary: str, articles: list, output_dir: str = "reports") -> str:
    """
    Generate a Markdown report with the summary and list of articles with citations,
    saving each report with a unique timestamp in the filename.

    Args:
        summary (str): The summarized text.
        articles (list): List of article dictionaries.
        output_dir (str): Directory to save the summary report.

    Returns:
        str: Path to the generated report.
    """
    # Ensure output directory ends with a slash and timestamp-based filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"summary_report_{timestamp}.md"
    output_path = f"{output_dir}/{filename}"

    # Create the directory if it doesn't exist
    import os
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
            citation = f"**Article {i}**: {authors}. _{source}_."
            if doi:
                citation += f" DOI: {doi}."
            if link:
                citation += f" [Link]({link})."
            f.write(f"- {citation}\n")

    return output_path