"""Email service using SMTP."""
import logging
import smtplib
from email.message import EmailMessage
from core.config import settings

log = logging.getLogger("email")

def send_contact_notification(to: str, name: str, email: str, subject: str | None, body: str) -> None:
    # Always log it as a backup
    log.info(f"Sending contact notification to {to} from {name} <{email}>")
    
    if not settings.SMTP_PASSWORD:
        log.warning("SMTP_PASSWORD not configured! Falling back to console logging.")
        return
        
    msg = EmailMessage()
    msg.set_content(
        f"You have received a new contact message from your Portfolio!\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Subject: {subject or 'No Subject'}\n\n"
        f"Message:\n{body}\n"
    )
    msg["Subject"] = f"Portfolio Contact: {subject or 'New Message'} from {name}"
    msg["From"] = settings.SMTP_USER
    msg["To"] = to
    msg["Reply-To"] = email

    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        log.info("Email notification sent successfully.")
    except Exception as e:
        log.error(f"Failed to send email notification: {e}")
