import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import base64
from email.utils import formataddr
import csv
import time
import random

# Path to your service account key JSON file
SERVICE_ACCOUNT_FILE = 'service_account_key.json'

# The email address of the user you want to impersonate (test2@gmail.com)

#USER_TO_IMPERSONATE = 'info.walidacja@'
USER_TO_IMPERSONATE = 'uzytkownik@edu.pl'
sender_name = "Instytut"

# Scopes needed for Gmail
SCOPES = ['https://mail.google.com/']

def create_message(sender, to, subject, html_body, attachment_path=None, image_paths=None):
    """Creates a MIME message object with HTML body, embedded images, and optional attachmentpromp"""
    message = MIMEMultipart('related')  # 'related' for embedded images
    message['to'] = to
    message['from'] = formataddr((sender_name, sender))
    message['subject'] = subject

    # Create the HTML part with embedded images
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    # Attach HTML body with embedded images
    html_part = MIMEText(html_body, 'html')
    msg_alternative.attach(html_part)

    # Attach images for embedding (like signature)
    if image_paths:
        for img_path in image_paths:
            with open(img_path, 'rb') as img_file:
                img_data = img_file.read()
            img_name = os.path.basename(img_path)
            img_mime = MIMEImage(img_data, name=img_name)
            img_mime.add_header('Content-ID', f'<{img_name}>')
            img_mime.add_header('Content-Disposition', 'inline', filename=img_name)
            message.attach(img_mime)

    # Attach file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        message.attach(part)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Sends an email message."""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


def main():
    """Authenticates with Gmail API using a service account and sends an email."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
        subject=USER_TO_IMPERSONATE  # Specify the user to impersonate
    )

    try:
        service = build('gmail', 'v1', credentials=creds)
        sender_email = USER_TO_IMPERSONATE

        name_and_email = os.path.join(os.path.expanduser("~"), "Desktop", "certs", "outlist.csv")
        with open(name_and_email, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = list(reader)  # Read all rows once
        total_email = len(rows)
        print("Total emails:", rows)
        start = 0
        file_index = 0

        while True:
            email_random_number = random.randint(5, 10)
            #email_random_number = email_random_number//2
            print("#" * 10)
            for _ in range(email_random_number):
                if file_index >= total_email:
                    break
                receiver_email = rows[file_index][0]

                
                subject = "zaświadczenie za udział w seminarium on-line"
                # subject = 'Certificate of participation: online seminar'
                # subject = "Zaświadczenie po szkoleniu: 'Ocena funkcjonalna: model, procedura, narzędzia. Szkolenie dla nauczycieli i nauczycielek pracujących w szkołach ponadpodstawowych'"

                # Path to HTML content
                content_path = os.path.join(os.path.expanduser("~"), "Desktop", "content.html")
                # content_path = os.path.join(os.path.expanduser("~"), "Desktop", "content — kopia.html")
                with open(content_path, "r", encoding='utf-8') as file:
                    body = file.read()

                # Path to attachment (optional)
                attachment_path = os.path.join(os.path.expanduser("~"), "Desktop", "certs", "pdfs", rows[file_index][1])
                print(attachment_path)
                # Path to signature image (should be referenced in HTML with <img src="cid:filename.jpg">)
                # signature_image_path = os.path.join(os.path.expanduser("~"), "Desktop", "footers", "julian.jpg")
                signature_image_path = os.path.join(os.path.expanduser("~"), "Desktop", "footers", "lena.jpg")
                    #lena.jpg
                message = create_message(
                    sender_email,
                    receiver_email,
                    subject,
                    body,
                    attachment_path=attachment_path,
                    image_paths=[signature_image_path]
                )
                send_message(service, 'me', message)
                file_index += 1

            start += email_random_number
            if start >= total_email:
                break
            sleep_duration = random.randint(20, 30)
            print(f'sleeping', end=' ')
            for i in range(sleep_duration, 0, -1):
                print(f"sleeping {i}", end=' ')
                # stdout_logger.info(f"sleeping {i} seconds...")
                time.sleep(1)
            print("\nResuming loop")


    except Exception as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()

