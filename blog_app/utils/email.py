import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from blog_app.core.config import settings


def send_verification_email(email: str, otp_code: str) -> bool:
    """Send verification email with OTP code."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_USER
        msg['To'] = email
        msg['Subject'] = "Email Verification"
        
        # Email body
        body = f"""
        <html>
        <body>
            <h2>Email Verification</h2>
            <p>Your verification code is: <strong>{otp_code}</strong></p>
            <p>This code will expire in 10 minutes.</p>
            <p>If you didn't request this verification, please ignore this email.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(settings.EMAIL_USER, email, text)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 