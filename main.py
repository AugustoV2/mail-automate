import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587  
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

RECIPIENTS_FILE = 'recipients.txt'
PDF_FILE = 'GDG.pdf'  # Replace with the path to your PDF file

SUBJECT = 'Invitation: GDG Solutions Challenge 2025 Bootcamp'

# Use HTML for the email body
BODY = '''<html>
<body>
<p><b>Respected Sir/Madam,</b></p>

<p><b>I hope this message finds you well.</b></p>

<p>On behalf of the <b>Google Developer Group (GDG) on Campus Community</b> at <b>Amal Jyothi College of Engineering, Kanjirappally</b>, we are pleased to extend an invitation to your esteemed institution to join us for the <b>GDG Solutions Challenge 2025 Bootcamp</b>. Our college has been selected to host this prestigious event, offering a unique platform for students to engage with cutting-edge Google technologies and develop innovative solutions addressing real-world challenges aligned with the United Nations' <b>Sustainable Development Goals (SDGs)</b>.</p>

<p><b>Event Overview:</b></p>

<p><b>GDG Solutions Challenge 2025:</b><br>
This global initiative inspires students to leverage Google technologies to create impactful solutions in areas such as education, healthcare, sustainability, and beyond.</p>

<p><b>Why Attend the Bootcamp?</b></p>

<ul>
<li><b>Expert Guidance:</b> Participate in hands-on training sessions led by Google experts.</li>
<li><b>Career Prospects:</b> Explore placement opportunities with leading companies, including Disney, HCL, and TCS.</li>
<li><b>Certification Support:</b> Gain access to exclusive Google Cloud Certification vouchers.</li>
<li><b>Competitive Rewards:</b> Compete for prizes worth ₹8 Lakhs.</li>
<li><b>Additional Perks:</b> Enjoy complimentary meals and exclusive Google merchandise.</li>
</ul>

<p><b>Bootcamp Details:</b></p>

<ul>
<li><b>Venue:</b> Amal Jyothi College of Engineering, Kanjirappally</li>
<li><b>Date:</b> 16th March</li>
<li><b>Registration:</b> <a href="https://bit.ly/4aYsQK6">https://bit.ly/4aYsQK6</a></li>
</ul>

<p><b>Please note that participation is open only to students registered for the GDG Solutions Challenge, and seats are limited. Early registration is encouraged.</b></p>

<p>For further information or any queries, please feel free to contact:</p>

<ul>
<li><b>Nevin Siby:</b> 9656052378</li>
<li><b>Hiba Nizar:</b> 7025463430</li>
</ul>

<p>We believe that your institution’s participation will greatly contribute to fostering collaborative efforts and innovation within our academic communities. Thank you for considering this invitation.</p>

<p>Yours sincerely,</p>

<p><b>Google Developer Group on Campus Community</b><br>
Amal Jyothi College of Engineering</p>
</body>
</html>'''

def send_email(sender, password, recipients, subject, body, pdf_file_path):
    try:
        print("Sender email:", SENDER_EMAIL)
        print("Sender password:", SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['Subject'] = subject

        # Use HTML for the email body
        msg.attach(MIMEText(body, 'html'))

        # Attach the PDF file
        with open(pdf_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(pdf_file_path)}',
            )
            msg.attach(part)

        # Add all recipients to the BCC field
        msg['Bcc'] = ', '.join(recipients)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(sender, password)

            # Send the email once with all recipients in BCC
            server.sendmail(sender, recipients, msg.as_string())
            print(f"Email sent to {len(recipients)} recipients in BCC.")

        print("Email sent successfully!")
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
        send_email(SENDER_EMAIL, SENDER_PASSWORD, recipients, SUBJECT, BODY, PDF_FILE)
    else:
        print("No recipients found or error reading the file.")