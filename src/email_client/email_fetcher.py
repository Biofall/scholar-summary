# src/email_client/email_fetcher.py
import imaplib
import email
from email.header import decode_header
from typing import List
from src.config import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_FOLDER
from src.utils.logger import logger

def connect_to_email():
    # Connect to the IMAP server and log in
    mail = imaplib.IMAP4_SSL(EMAIL_SERVER)
    mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    return mail

def fetch_unread_scholar_emails() -> List[str]:
    """
    Fetch unread Google Scholar alert emails from the inbox.
    Returns a list of raw HTML email bodies.
    """

    mail = connect_to_email()
    # Select the mailbox (read-only=False so we can mark as read if we want)
    mail.select(EMAIL_FOLDER, readonly=False)

    # Search for unread messages
    status, messages = mail.search(None, '(UNSEEN FROM "scholaralerts-noreply@google.com")')
    if status != 'OK':
        logger.error("Could not search mailbox.")
        return []

    email_ids = messages[0].split()
    html_bodies = []

    for eid in email_ids:
        # Fetch the email by ID
        status, data = mail.fetch(eid, '(RFC822)')
        if status != 'OK':
            logger.warning(f"Failed to fetch email with ID {eid.decode()}")
            continue

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # The email might be multipart. We need to find the HTML part.
        html_content = None
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/html':
                    charset = part.get_content_charset() or 'utf-8'
                    html_content = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
        else:
            # If not multipart, check if it's HTML directly
            if msg.get_content_type() == 'text/html':
                charset = msg.get_content_charset() or 'utf-8'
                html_content = msg.get_payload(decode=True).decode(charset, errors='replace')

        if html_content:
            html_bodies.append(html_content)
            # Mark the email as seen (read)
            mail.store(eid, '+FLAGS', '\\Seen')
        else:
            logger.warning(f"No HTML part found in email with ID {eid.decode()}")

    mail.close()
    mail.logout()

    return html_bodies