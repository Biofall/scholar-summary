import sys
from src.utils.logger import logger
from src.email_client.email_fetcher import fetch_unread_scholar_emails
from src.email_client.email_parser import parse_scholar_alert
from src.data_store.db_handler import store_articles, get_all_articles
from src.summarizer.summarizer import summarize_articles
from src.renderer.report_generator import generate_summary_report
from src.enrichment.crossref import enrich_article_data

def main():
    logger.info("Starting Scholar Summarizer...")

    # Check for '--force' argument
    force_summary = '--force' in sys.argv

    # 1. Fetch unread emails
    html_bodies = fetch_unread_scholar_emails()
    logger.info(f"Fetched {len(html_bodies)} unread scholar alert emails.")

    all_new_articles = []

    # 2. Parse and enrich articles from each HTML body
    for html_body in html_bodies:
        parsed_articles = parse_scholar_alert(html_body)
        logger.info(f"Parsed {len(parsed_articles)} articles from one email.")

        # Enrich articles
        enriched_articles = [enrich_article_data(article) for article in parsed_articles]

        # 3. Store articles to avoid duplicates
        new_articles = store_articles(enriched_articles)
        logger.info(f"Stored {len(new_articles)} new articles (after deduplication).")

        all_new_articles.extend(new_articles)

    # If no new articles and not forced, exit
    if not all_new_articles and not force_summary:
        logger.info("No new articles to summarize. Exiting.")
        return

    # If forced, but no new articles, try summarizing all existing articles
    if not all_new_articles and force_summary:
        logger.info("No new articles found, but --force was used. Summarizing all stored articles.")
        all_articles = get_all_articles()
        if not all_articles:
            logger.info("No articles are stored at all. Nothing to summarize.")
            return
        articles_to_summarize = all_articles
    else:
        articles_to_summarize = all_new_articles

    # 4. Summarize articles
    summary = summarize_articles(articles_to_summarize)

    # 5. Generate report
    report_path = generate_summary_report(summary, articles_to_summarize)
    logger.info(f"Summary report generated at: {report_path}")

if __name__ == "__main__":
    main()