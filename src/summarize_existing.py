# summarize_existing.py
from src.data_store.db_handler import load_articles
from src.summarizer.summarizer import summarize_articles
from src.renderer.report_generator import generate_summary_report
from src.utils.logger import logger

def main():
    articles = load_articles()
    if not articles:
        logger.info("No articles found in articles.json. Nothing to summarize.")
        return
    summary = summarize_articles(articles)
    report_path = generate_summary_report(summary, articles)
    logger.info(f"Summary report generated at: {report_path}")

if __name__ == "__main__":
    main()