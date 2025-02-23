import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587  
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


RECIPIENTS_FILE = 'recipients.txt'


SUBJECT = 'Myreee'
BODY = 'Pyhton mail automate cheyydh :)'

def send_email(sender, password, recipients, subject, body):
    try:
        print("Sender email:", SENDER_EMAIL)
        print("Sender password:", SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(sender, password)

           
            for recipient in recipients:
                msg['To'] = recipient
                server.sendmail(sender, recipient, msg.as_string())
                print(f"Email sent to: {recipient}")

            print("All emails sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def read_recipients(file_path, max_emails=50):
    try:
        with open(file_path, 'r') as file:
            recipients = [line.strip() for line in file.readlines() if line.strip()]
            return recipients[:max_emails]  
    except Exception as e:
        print(f"Error reading recipients file: {e}")
        return []

if __name__ == '__main__':
   
    recipients = read_recipients(RECIPIENTS_FILE, max_emails=50)

    if recipients:
        send_email(SENDER_EMAIL, SENDER_PASSWORD, recipients, SUBJECT, BODY)
    else:
        print("No recipients found or error reading the file.")