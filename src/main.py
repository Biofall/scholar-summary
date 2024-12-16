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
    total_emails = len(html_bodies)
    if total_emails == 0:
        logger.info("No unread scholar alert emails found. Exiting.")
        return

    logger.info(f"Found {total_emails} unread scholar alert emails. Beginning processing...")
    all_new_articles = []

    # 2. Parse and enrich articles from each email with a progress meter
    for i, html_body in enumerate(html_bodies, start=1):
        logger.info(f"Processing email {i}/{total_emails}...")

        parsed_articles = parse_scholar_alert(html_body)
        num_parsed = len(parsed_articles)
        logger.info(f"Email {i}/{total_emails}: Parsed {num_parsed} articles.")

        # Enrich articles
        enriched_articles = [enrich_article_data(article) for article in parsed_articles]

        # Store articles to avoid duplicates
        new_articles = store_articles(enriched_articles)
        num_new = len(new_articles)
        num_skipped = num_parsed - num_new

        logger.info(
            f"Email {i}/{total_emails}: Added {num_new} new articles, "
            f"skipped {num_skipped} duplicates."
        )

        all_new_articles.extend(new_articles)

    # After processing all emails
    total_new = len(all_new_articles)
    if total_new == 0 and not force_summary:
        logger.info("No new articles added and not forced to summarize. Exiting.")
        return

    # If forced, but no new articles, summarize all stored articles
    if total_new == 0 and force_summary:
        logger.info("No new articles found, but --force was used. Summarizing all stored articles.")
        all_articles = get_all_articles()
        if not all_articles:
            logger.info("No articles are stored at all. Nothing to summarize.")
            return
        articles_to_summarize = all_articles
    else:
        articles_to_summarize = all_new_articles

    # Summarize articles
    logger.info("Summarizing articles...")
    summary = summarize_articles(articles_to_summarize)

    # Generate report
    report_path = generate_summary_report(summary, articles_to_summarize)
    logger.info(f"Summary report generated at: {report_path}")

if __name__ == "__main__":
    main()