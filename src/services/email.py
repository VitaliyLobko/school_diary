from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import create_email_token

conf = ConnectionConfig(
    MAIL_USERNAME="school_diary@meta.ua",
    MAIL_PASSWORD="123",
    MAIL_FROM="school_diary@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="School diary app",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """Send verification email or, when running locally, log the link.

    Most development environments won't have a real SMTP server configured,
    and the default credentials above are placeholders.  We therefore always
    construct the confirmation URL and print it to the console; if the mailer
    fails to deliver due to connection problems we log the error too but the
    link remains visible so testing is still possible.
    """
    token_verification = create_email_token({"sub": email})
    link = f"{host}confirmed_email/{token_verification}"
    # always log the verification link so the developer can copy it
    print(f"[email] verification link for {email}: {link}")

    # attempt to send over SMTP; errors are non‑fatal for dev
    try:
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email.html")
    except ConnectionErrors as err:
        # print error but don't re‑raise; the link has already been shown
        print("failed to send email, see verification link above", err)
