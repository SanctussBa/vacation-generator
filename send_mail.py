import smtplib
from email.mime.text import MIMEText


def send_mail(name, email, message):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '62157e44d1c5c9'
    password = '36efbd0b116fe1'
    message = "<h3>New message from Generator web app</h3><ul><li>Name: {}</li><li>emial: {}</li><li>Message: {}</li></ul>".format(name, email, message)

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Comments from generator app'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
