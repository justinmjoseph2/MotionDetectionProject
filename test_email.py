import smtplib
from email.message import EmailMessage

def send_test_email():
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'justinmjoseph222@gmail.com'
    EMAIL_HOST_PASSWORD = 'kugm hubo rack ofqt'
    
    msg = EmailMessage()
    msg['Subject'] = 'Test Email'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = 'justin.23pmc132@mariancollege.org'
    msg.set_content('This is a test email.')

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
        print("Test email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_test_email()
