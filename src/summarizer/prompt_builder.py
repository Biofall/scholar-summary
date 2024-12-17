# src/summarizer/prompt_builder.py

def build_prompt(articles):
    """
    Build a prompt to be sent to the LLM tailored to the company's context.
    The prompt will:
    - Provide context about the company's focus on integrating behavioral and physiological monitoring from passive sensing sources
      to predict mental and neurological health treatments and disease progression using ML.
    - Categorize the provided scholarly articles into broad, context-relevant categories.
    - Provide a comprehensive summary synthesizing main findings, highlights, common themes, differences, and
      important nuances within each category.
    - Include short summaries for each individual paper.
    - Use consistent article citations (e.g., Article X) based on the numbered list.
    - Conclude with trends observed across the papers.
    - Suggest specific papers for closer reading and rationale based on the company's focus.
    """

    instructions = (
        "You are a scholarly assistant working for a company that integrates behavioral and physiological monitoring from multiple "
        "passive sensing sources to better predict mental and neurological health treatments and disease progression, "
        "leveraging machine learning (ML) technologies. I will provide you with several scholarly articles, each containing "
        "a title, authors, source, abstract/snippet, and possibly a DOI. Your tasks are as follows:\n\n"
        "1. **Categorization:** Organize the articles into broad categories that align with our company's focus on behavioral and physiological "
        "monitoring, wearables and passive sensing, ML applications, mental health, and neurological/psychiatric disease progression. Each "
        "category should have a title. The categories should be logical and relevant based on the provided context. At the top of each "
        "category, provide a summary of that category. The summary should have a 2 sections: 1) Synthesis of the main findings and "
        "highlights of the major themes and 2) Important nuances and differences across the studies. Cite the papers as they are relevant "
        "in the summary as (Article X, Auhor Lastname), where X corresponds to the article's number in the provided list and Lastname is the "
        "first author's last name.\n\n"
        "2. **Individual Paper Summaries:** After the summary for the category, provide a concise summary for each study in the category. The "
        " format for the summary should be: Article X: Summary. You do not need to give links or authors.\n\n"
        "3. **Suggestions for Further Reading:** Recommend specific papers for closer examination, explaining why they are particularly relevant "
        "given our company's focus.\n\n"
        "Ensure that every article that is referenced matches its number and author to the provided list. . Check again at the end before "
        "proceeding to ensure that no hallucinations or mistakes were made." 
    )

    article_strs = []
    for i, article in enumerate(articles, start=1):
        # Extract available fields, using defaults if missing
        title = article.get("title", "No Title")
        authors = ", ".join(article.get("authors", [])) if article.get("authors") else "Unknown authors"
        source = article.get("source", "Unknown source")
        doi = article.get("doi", "")
        snippet = article.get("snippet", "")

        # Format each article block
        art_block = f"**Article {i}:**\n" \
                    f"**Title:** {title}\n" \
                    f"**Authors:** {authors}\n" \
                    f"**Source:** {source}\n"
        if doi:
            art_block += f"**DOI:** {doi}\n"
        art_block += f"**Abstract/Snippet:** {snippet}\n"
        article_strs.append(art_block.strip())

    articles_text = "\n\n".join(article_strs)

    prompt = (
        f"{instructions}\n\n"
        f"### Provided Articles:\n\n"
        f"{articles_text}\n\n"
        f"### Please provide the following:\n"
        f"1. Categorize the articles.\n"
        f"2. Provide a comprehensive summary for each category.\n"
        f"3. Include short summaries for each individual paper within the category.\n"
        f"4. Draw conclusoins about trends, gaps, and opportunities acorss the papers.\n"
        f"5. Suggest specific papers to read closely and explain why they are relevant.\n"
    )
    return prompt