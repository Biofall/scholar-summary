# Scholar Summary

**Scholar Summary** is a pipeline designed to transform Google Scholar alert emails into rich, synthesized summaries of newly published research. With a few automated steps, it fetches your latest Scholar alerts, extracts article metadata, enriches them via external APIs like CrossRef, and then uses ChatGPT to craft a consolidated summary report—complete with citations. Perfect for staying on top of the literature in your field without trawling through dozens of separate alerts.

## What This Tool Does

- **Fetches & Parses Emails:** Connects to your Google Scholar alerts (now via the Gmail API and OAuth2) and pulls down unread alert emails.
- **Extracts Articles:** Uses HTML parsing to identify article titles, authors, sources, and snippets.
- **Enrichment:** CrossRef and other metadata services fill in missing details such as DOIs, publication dates, and more complete abstracts.
- **Summarization via ChatGPT:** Feeds the curated set of articles into ChatGPT to produce a polished, multi-article summary that cites each source.
- **Report Generation:** Outputs a Markdown report summarizing key findings, with a reference list for easy follow-up reading.

## Why You’ll Love It

1. **Time-Saving:** Stop manually scanning each alert for interesting articles. Let this pipeline gather and highlight the most relevant findings for you.
2. **Contextual Understanding:** By summarizing multiple articles together, you gain a holistic understanding of recent developments in your field.
3. **Flexible & Extensible:** Tweak the parsing logic, enrich using different APIs, or alter the summarization prompt. This project is designed to grow with your needs.

## Getting Started

### Prerequisites

- **Python 3.9+**  
- A **Gmail account** set up with the Gmail API and OAuth2 credentials.
- **OpenAI API Key** for ChatGPT access.

You’ll also need to install dependencies listed in `requirements.txt`.

### Setup Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/scholar-summarizer.git
   cd scholar-summarizer
   ```
   
2. **Create a Virtual Environment & Install Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
- Rename or create user.env (or .env) at the project root:
   ```bash
   cp user.env.example user.env
   ```
- Fill in the your relevant info for the user.env file
   - Add your OPENAI_API_KEY and ensure your Gmail username/pass. See optional steps below if 2FA and Google App Passwords need to be setup.
- See config.py for environment variable usage.

#### OPTIONAL - Set up a Google App Password
---
If you have **Two-Factor Authentication (2FA)** enabled on your Google account, you’ll need to create an App Password to allow Scholar Summarizer to access your Gmail account via the Gmail API.
Steps to Create a Google App Password:
1. Sign in to Your Google Account:
- Navigate to your Google Account.
2. Access Security Settings:
- From the left-hand menu, select Security.
3. Ensure 2FA is Enabled:
- Under the “Signing in to Google” section, make sure 2-Step Verification is ON. If it’s not, you’ll need to enable it first.
4. Create an App Password:
- Click on App passwords. (This option appears only if 2FA is enabled.)
- You might be prompted to enter your password again for security.
- In the “Select app” dropdown, choose Other (Custom name).
- Enter a name like ScholarSummarizer and click Generate.
- Google will provide a 16-character app password. Copy this password as you’ll need it for the user.env file.
5. Update user.env with the App Password
- Open your user.env file.
- Replace the Gmail password field with the newly generated app password.
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GMAIL_USER=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   ```
---

4. **Fetch & Summarize:**
   ```bash
   python -m src.main
   ```
This will:
- Fetch unread Scholar alerts.
- Parse and enrich article data.
- Summarize new findings.
- Generate output_summary.md with your synthesized report.

**Forcing a Summary When No New Articles Appear**

Run:
   ```bash
   python -m src.main --force
   ```
This command will create a summary of all stored articles, even if no new ones were fetched today.

File Structure
```
scholar-summarizer/
├─ user.env.example      # Environment variables (excluded from version control)
├─ data/
│  ├─ articles.json      # Stored articles
├─ src/
│  ├─ main.py            # Entry point
│  ├─ config.py          # Configuration handling from env variables
│  ├─ email_client/
│  │  ├─ gmail_auth.py   # Gmail API auth logic
│  │  ├─ email_fetcher.py# Fetching emails via Gmail API
│  │  ├─ email_parser.py # Parsing Scholar alert HTML to extract articles
│  ├─ data_store/
│  │  ├─ db_handler.py   # Stores & retrieves articles from JSON
│  ├─ summarizer/
│  │  ├─ prompt_builder.py
│  │  ├─ summarizer.py   # Summarizes articles via OpenAI API
│  ├─ enrichment/
│  │  ├─ crossref.py     # Enriches metadata from CrossRef
│  ├─ renderer/
│  │  ├─ report_generator.py # Generates the final markdown summary report
│  ├─ utils/
│  │  ├─ logger.py       # Logging configuration
└─ tests/
   ├─ test_*.py          # Unit tests
```

Customization
- Prompts: Adjust prompt_builder.py to refine the tone and depth of the summary.
- Metadata Sources: Add or modify enrichment strategies in crossref.py to fetch more or different metadata.
- Storage: Switch from JSON to a database if you need more robust article management.

Troubleshooting
- No Emails Fetched: Check your Gmail label for unread emails.
- Invalid Credentials: Use app passwords or ensure OAuth2 flow is complete. Will add instructures later
- Source Fields Not Cleaned: Update your parsing logic in email_parser.py if Google Scholar changes its formatting.
- OpenAI Errors: Ensure your OPENAI_API_KEY is valid and you have API credits/permissions.

Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve. We value code quality, clear commit messages, and well-written documentation.

Scholar Summarizer: Automated literature curation that saves you time and keeps you at the forefront of your research domain.

