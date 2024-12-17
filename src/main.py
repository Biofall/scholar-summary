import sys
from math import ceil
from src.utils.logger import logger
from src.email_client.email_fetcher import fetch_unread_scholar_emails
from src.email_client.email_parser import parse_scholar_alert
from src.data_store.db_handler import store_articles, get_all_articles, load_articles
from src.summarizer.summarizer import summarize_articles
from src.renderer.report_generator import generate_summary_report
from src.enrichment.crossref import enrich_article_data

MAX_ARTICLES_PER_SET = 30

def main():
    logger.info("Starting Scholar Summarizer...")

    summarize_only = '--summarize-only' in sys.argv

    if summarize_only:
        # Summarize-only mode: no fetching, just load and summarize existing articles
        logger.info("Running in summarize-only mode. Loading articles from articles.json...")
        all_articles = load_articles()
        if not all_articles:
            logger.info("No articles found in articles.json. Nothing to summarize.")
            return
        articles_to_summarize = all_articles
    else:
        # Normal mode: Fetch and parse emails, then summarize new articles if any
        html_bodies = fetch_unread_scholar_emails()
        total_emails = len(html_bodies)
        if total_emails == 0:
            logger.info("No unread scholar alert emails found. Exiting.")
            return

        logger.info(f"Found {total_emails} unread scholar alert emails. Beginning processing...")
        all_new_articles = []

        for i, html_body in enumerate(html_bodies, start=1):
            logger.info(f"Processing email {i}/{total_emails}...")
            parsed_articles = parse_scholar_alert(html_body)
            num_parsed = len(parsed_articles)
            logger.info(f"Email {i}/{total_emails}: Parsed {num_parsed} articles.")

            enriched_articles = [enrich_article_data(article) for article in parsed_articles]

            new_articles = store_articles(enriched_articles)
            num_new = len(new_articles)
            num_skipped = num_parsed - num_new

            logger.info(
                f"Email {i}/{total_emails}: Added {num_new} new articles, "
                f"skipped {num_skipped} duplicates."
            )
            all_new_articles.extend(new_articles)

        if len(all_new_articles) == 0:
            logger.info("No new articles added. Exiting.")
            return
        else:
            articles_to_summarize = all_new_articles

    # At this point, we have articles_to_summarize ready in both modes
    total_articles = len(articles_to_summarize)
    if total_articles == 0:
        logger.info("No articles to summarize. Exiting.")
        return

    logger.info(f"Preparing to summarize {total_articles} articles in sets of {MAX_ARTICLES_PER_SET}.")

    # Split into sets of MAX_ARTICLES_PER_SET
    num_sets = ceil(total_articles / MAX_ARTICLES_PER_SET)
    if num_sets == 1 and total_articles <= MAX_ARTICLES_PER_SET:
        # If only one set needed, just summarize directly
        summary = summarize_articles(articles_to_summarize)
        report_path = generate_summary_report(summary, articles_to_summarize)
        logger.info(f"Summary report generated at: {report_path}")
    else:
        # Multiple sets
        logger.info(f"Splitting into {num_sets} sets of up to {MAX_ARTICLES_PER_SET} articles each.")
        for i in range(num_sets):
            start = i * MAX_ARTICLES_PER_SET
            end = start + MAX_ARTICLES_PER_SET
            subset = articles_to_summarize[start:end]
            logger.info(f"Summarizing set {i+1}/{num_sets} with {len(subset)} articles.")
            subset_summary = summarize_articles(subset)

            chunk_report_path = f"output_summary_chunk_{i+1}.md"
            chunk_report_path = generate_summary_report(subset_summary, subset, filename_prefix=f"chunk_{i+1}")
            logger.info(f"Report for set {i+1}/{num_sets} generated at: {chunk_report_path}")

if __name__ == "__main__":
    main()