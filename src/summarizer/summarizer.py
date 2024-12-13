# src/summarizer/summarizer.py
import openai
from src.config import OPENAI_API_KEY
from src.summarizer.prompt_builder import build_prompt

def summarize_articles(articles):
    openai.api_key = OPENAI_API_KEY

    prompt = build_prompt(articles)

    # Using gpt-3.5-turbo or gpt-4 depending on your model availability.
    # Replace 'gpt-3.5-turbo' with 'gpt-4' if you have access.
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
    )

    summary = response.choices[0].message.content.strip()
    return summary