# src/summarizer/summarizer.py
import openai
from src.config import OPENAI_API_KEY
from src.summarizer.prompt_builder import build_prompt
from src.utils.logger import logger
import math

MAX_ARTICLES_PER_BATCH = 30  # adjust this based on trial and error

def summarize_articles(articles):
    openai.api_key = OPENAI_API_KEY

    # If too many articles, summarize in batches
    if len(articles) > MAX_ARTICLES_PER_BATCH:
        logger.info(f"Too many articles ({len(articles)}) to summarize at once. Splitting into batches.")
        
        batch_size = MAX_ARTICLES_PER_BATCH
        num_batches = math.ceil(len(articles) / batch_size)
        batch_summaries = []

        for i in range(num_batches):
            start = i * batch_size
            end = start + batch_size
            batch = articles[start:end]
            logger.info(f"Summarizing batch {i+1}/{num_batches} with {len(batch)} articles.")
            batch_summary = summarize_batch(batch)
            batch_summaries.append(batch_summary)

        # Now summarize the batch summaries themselves
        logger.info(f"Summarizing {len(batch_summaries)} batch summaries into a final summary.")
        final_summary = summarize_batch_summaries(batch_summaries)
        return final_summary
    else:
        # If we have a manageable number of articles, summarize directly
        return summarize_batch(articles)

MAX_SNIPPET_LENGTH = 500  # characters

def summarize_batch(articles_batch):
    # Truncate long snippets
    for a in articles_batch:
        if len(a.get("snippet", "")) > MAX_SNIPPET_LENGTH:
            a["snippet"] = a["snippet"][:MAX_SNIPPET_LENGTH] + "..."
    
    prompt = build_prompt(articles_batch)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,  # reduce max_tokens if needed
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except openai.error.InvalidRequestError as e:
        # If you still hit the limit, consider retrying with fewer articles or shorter snippets
        logger.error(f"Request too large: {e}. Trying fewer articles or shorter snippets next time.")
        return "Summary could not be generated due to token limits."

def summarize_batch_summaries(batch_summaries):
    # Summarize the summaries themselves
    # Treat each batch summary as "article snippet" for simplicity
    pseudo_articles = [{"title": f"Batch {i+1}", "authors": [], "source": "SummaryBatch", "snippet": s, "publication_date": ""} 
                       for i, s in enumerate(batch_summaries)]
    return summarize_batch(pseudo_articles)