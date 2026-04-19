"""Email service - console log only (no external SMTP per user request)."""
import logging

log = logging.getLogger("email")


def send_contact_notification(to: str, name: str, email: str, subject: str | None, body: str) -> None:
    log.info(
        "\n===== NEW CONTACT MESSAGE =====\n"
        "To:      %s\n"
        "From:    %s <%s>\n"
        "Subject: %s\n"
        "Body:    %s\n"
        "================================\n",
        to, name, email, subject or "(no subject)", body,
    )
