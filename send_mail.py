import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

to = input("To email: ")
subject = input("Subject: ")
content = input("Content: ")

message = Mail(
    from_email='boyuanliu6@yahoo.com',
    to_emails=to,
    subject=subject,
    html_content=content)
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)