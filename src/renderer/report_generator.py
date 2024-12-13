# src/renderer/report_generator.py

def generate_summary_report(summary: str, articles: list, output_path: str = "output_summary.md") -> str:
    """
    Generate a Markdown report with the summary and list of articles with citations.

    Args:
        summary (str): The summarized text.
        articles (list): List of article dictionaries.
        output_path (str): Path to save the summary report.

    Returns:
        str: Path to the generated report.
    """
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