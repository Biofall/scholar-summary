# src/summarizer/prompt_builder.py

def build_prompt(articles):
    """
    Build a prompt to be sent to the LLM.
    The prompt will:
    - Explain that we have multiple scholarly articles.
    - Instruct the model to summarize key findings, highlight common themes, differences, and interesting points.
    - Require citations for claims (e.g., (Article 1)) corresponding to the article order in the list.
    - Conclude with a summary statement.
    """

    instructions = (
        "You are a scholarly assistant. I will provide you with several articles, each with a title, authors, source, "
        "abstract/snippet, and possibly a DOI. Your task is to write a comprehensive summary that synthesizes their main "
        "findings, highlights any common themes, differences, and important nuances. Whenever you refer to information "
        "from a given article, cite it as (Article X) where X is the article number in the list. After summarizing, "
        "provide a brief conclusion. Write in a neutral, academic tone."
    )

    article_strs = []
    for i, article in enumerate(articles, start=1):
        # Some fields may be missing; we'll just include what we have.
        title = article.get("title", "No Title")
        authors = ", ".join(article.get("authors", [])) if article.get("authors") else "Unknown authors"
        source = article.get("source", "Unknown source")
        doi = article.get("doi", "")
        snippet = article.get("snippet", "")

        # Format each article block
        art_block = f"Article {i}:\nTitle: {title}\nAuthors: {authors}\nSource: {source}\n"
        if doi:
            art_block += f"DOI: {doi}\n"
        art_block += f"Abstract/Snippet: {snippet}\n"
        article_strs.append(art_block.strip())

    articles_text = "\n\n".join(article_strs)

    prompt = f"{instructions}\n\n{articles_text}\n\nPlease now produce the summary and conclusion."
    return prompt