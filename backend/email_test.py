import smtplib
from email.message import EmailMessage

# gmail account details:
# thearguswebsite@gmail.com
# vthuR*4td0@W

email_address = 'thearguswebsite@gmail.com'
email_password = 'vthuR*4td0@W'

msg = EmailMessage()
msg['Subject'] = "Test Email"
msg['From'] = email_address
msg['To'] = 'adam247866@gmail.com'
msg.set_content("Test email message")

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(email_address, email_password)
server.send_message(msg)
server.close()