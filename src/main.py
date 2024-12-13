from src.utils.logger import logger
from src.email_client.email_fetcher import fetch_unread_scholar_emails
from src.email_client.email_parser import parse_scholar_alert
from src.data_store.db_handler import store_articles
from src.summarizer.summarizer import summarize_articles
from src.renderer.report_generator import generate_summary_report
from src.enrichment.crossref import enrich_article_data

def main():
    logger.info("Starting Scholar Summarizer...")

    # 1. Fetch unread emails from scholar_alerts folder
    html_bodies = fetch_unread_scholar_emails()
    logger.info(f"Fetched {len(html_bodies)} unread scholar alert emails.")

    all_new_articles = []

    # 2. Parse and enrich articles from each HTML body
    for html_body in html_bodies:
        parsed_articles = parse_scholar_alert(html_body)
        logger.info(f"Parsed {len(parsed_articles)} articles from one email.")

        # Enrich articles
        enriched_articles = []
        for article in parsed_articles:
            enriched = enrich_article_data(article)
            enriched_articles.append(enriched)

        # 3. Store articles to avoid duplicates
        new_articles = store_articles(enriched_articles)
        logger.info(f"Stored {len(new_articles)} new articles (after deduplication).")

        all_new_articles.extend(new_articles)

    if not all_new_articles:
        logger.info("No new articles to summarize. Exiting.")
        return

    # 4. Summarize articles
    summary = summarize_articles(all_new_articles)

    # 5. Generate report
    report_path = generate_summary_report(summary, all_new_articles)
    logger.info(f"Summary report generated at: {report_path}")

if __name__ == "__main__":
    main()