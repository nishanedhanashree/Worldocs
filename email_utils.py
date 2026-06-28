import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv(override=True)

def _get_conf() -> ConnectionConfig:
    """Build a fresh ConnectionConfig using current env vars every time."""
    load_dotenv(override=True)
    return ConnectionConfig(
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME", "dummy_user"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD", "dummy_password"),
        MAIL_FROM=os.environ.get("MAIL_FROM", "noreply@worldocs.com"),
        MAIL_FROM_NAME="Worldocs",
        MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
        MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
    )

async def send_reset_password_email(email_to: EmailStr, token: str):
    html_content = f"""
    <div style="font-family:Arial,sans-serif; max-width:480px; margin:auto; padding:32px; background:#f8faff; border-radius:12px; border:1px solid #e0e7ff;">
      <h2 style="color:#4f46e5; margin-bottom:4px;">&#128274; Worldocs Password Reset</h2>
      <p style="color:#6b7280; margin-top:0;">You requested a password reset for your Worldocs account.</p>
      <p style="color:#1e1b4b; font-weight:600; margin-bottom:8px;">Your One-Time Password (OTP):</p>
      <div style="background:#eef2ff; border:2px solid #6366f1; border-radius:10px; padding:20px; text-align:center; margin:16px 0;">
        <span style="font-size:40px; font-weight:800; letter-spacing:12px; color:#4f46e5; font-family:monospace;">{token}</span>
      </div>
      <p style="color:#ef4444; font-size:0.88rem; font-weight:600;">&#9203; This OTP expires in <strong>10 minutes</strong>.</p>
      <p style="color:#6b7280; font-size:0.85rem;">Enter this OTP on the reset page along with your email and new password.</p>
      <hr style="border:none; border-top:1px solid #e0e7ff; margin:20px 0;">
      <p style="color:#9ca3af; font-size:0.78rem;">If you did not request this, please ignore this email. Your account is safe.</p>
    </div>
    """
    
    message = MessageSchema(
        subject="🔐 Worldocs Password Reset OTP",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )
    
    conf = _get_conf()
    fm = FastMail(conf)
    
    # If the dummy env vars are active, suppress failing connections and let it print safely to console instead.
    if conf.MAIL_USERNAME == "dummy_user":
        print(f"--- DUMMY EMAIL DISPATCH ---")
        print(f"TO: {email_to}")
        print(f"CONTENT: {html_content}")
        print(f"--- END DUMMY EMAIL DISPATCH ---")
        return
        
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        # Optionally re-raise or handle failure

async def send_forgot_username_email(email_to: EmailStr, username: str):
    html_content = f"""
    <h2>Worldocs – Username Reminder</h2>
    <p>You requested your username for the account registered with this email.</p>
    <p>Your username is:</p>
    <div style="background-color:#e0e7ff;padding:12px 20px;margin:12px 0;font-family:monospace;font-size:18px;font-weight:bold;border-radius:8px;letter-spacing:1px;">
        {username}
    </div>
    <p>If you did not request this, please ignore this email.</p>
    """

    message = MessageSchema(
        subject="Worldocs: Your Username",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )

    conf = _get_conf()
    fm = FastMail(conf)

    if conf.MAIL_USERNAME == "dummy_user":
        print(f"--- DUMMY EMAIL DISPATCH (forgot-username) ---")
        print(f"TO: {email_to}  USERNAME: {username}")
        print(f"--- END ---")
        return

    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending forgot-username email: {e}")


def send_pdf_email(recipient_email: str, filename: str, pdf_bytes: bytes, sender_name: str = "Worldocs"):
    """Send a translated PDF as an email attachment to any recipient using smtplib."""
    load_dotenv(override=True)
    mail_user   = os.environ.get("MAIL_USERNAME", "dummy_user")
    mail_pass   = os.environ.get("MAIL_PASSWORD", "")
    mail_from   = os.environ.get("MAIL_FROM", mail_user)
    mail_server = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    mail_port   = int(os.environ.get("MAIL_PORT", 587))

    if mail_user == "dummy_user":
        print(f"--- DUMMY PDF EMAIL ---  TO: {recipient_email}  FILE: {filename}")
        return

    msg = MIMEMultipart()
    msg["From"]    = f"{sender_name} <{mail_from}>"
    msg["To"]      = recipient_email
    msg["Subject"] = f"📄 Worldocs – Your Translated Document: {filename}"

    body = f"""\
<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;padding:32px;
            background:#f8faff;border-radius:12px;border:1px solid #e0e7ff;">
  <h2 style="color:#4f46e5;margin-bottom:4px;">📄 Worldocs Translation Ready</h2>
  <p style="color:#6b7280;margin-top:0;">A translated document has been shared with you via Worldocs.</p>
  <div style="background:#eef2ff;border:2px solid #6366f1;border-radius:10px;
              padding:16px 20px;margin:16px 0;">
    <strong style="color:#4f46e5;">File:</strong>
    <span style="font-family:monospace;font-size:1rem;color:#1e1b4b;"> {filename}</span>
  </div>
  <p style="color:#374151;">The translated PDF is attached to this email. Open it with any PDF viewer.</p>
  <hr style="border:none;border-top:1px solid #e0e7ff;margin:20px 0;">
  <p style="color:#9ca3af;font-size:0.78rem;">
    Sent via <strong>Worldocs</strong> – AI-Powered Document Translation.
    If you were not expecting this, you can safely ignore it.
  </p>
</div>"""

    msg.attach(MIMEText(body, "html"))

    # Attach the PDF
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    safe_filename = filename if filename.endswith(".pdf") else filename + ".pdf"
    part.add_header("Content-Disposition", f'attachment; filename="{safe_filename}"')
    msg.attach(part)

    with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.login(mail_user, mail_pass)
        server.sendmail(mail_from, recipient_email, msg.as_string())
    print(f"[email] PDF sent to {recipient_email}: {filename}")
