import cv2
import smtplib
from email.message import EmailMessage
import os
import sys
import django
import logging
import time

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MotionDetectionProject.settings')
django.setup()

from django.conf import settings
from detection.models import Subscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SMTP connection
smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
smtp_server.starttls()
smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

last_email_time = 0
interval = 15  # seconds

def send_email(image_path):
    global last_email_time

    current_time = time.time()
    if current_time - last_email_time < interval:
        return

    subscribers = Subscriber.objects.all()
    if not subscribers:
        return

    msg = EmailMessage()
    msg['Subject'] = 'Motion Detected'
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = [subscriber.email for subscriber in subscribers]
    msg.set_content('Motion has been detected. See the attached image for details.')

    with open(image_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename='motion.jpg')

    try:
        logger.info("Sending email...")
        smtp_server.send_message(msg)
        logger.info("Email sent successfully.")
        last_email_time = current_time  # Update last email time
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def motion_detection():
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            image_path = 'motion.jpg'
            cv2.imwrite(image_path, frame1)
            send_email(image_path)

        cv2.imshow('feed', frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(10) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motion_detection()

# Close SMTP connection after the program stops
smtp_server.quit()
