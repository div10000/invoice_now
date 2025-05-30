import smtplib
from email.message import EmailMessage

def send_email_with_attachment(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'  # Replace with your sender email
    msg['To'] = to_email
    msg.set_content(body)

    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = attachment_path.split('/')[-1]

    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('2203051050178@paruluniversity.ac.in', 'wfab wvol khgv ujdm')  # Replace with your email credentials
        smtp.send_message(msg)
