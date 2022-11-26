import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# gmail account details:
# thearguswebsite@gmail.com
# argusnotifier@yahoo.com
# vthuR*4td0@W
# gmail app password: saygdrmykwexunhf

port = 587
server = "smtp.gmail.com"
smtp_user = "thearguswebsite@gmail.com"
to_address = "rutledgea20@gmail.com"
smtp_password = "saygdrmykwexunhf"
subject = "hello there"
body = "testing this email's capabilities"

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = smtp_user
msg["To"] = to_address
msg.attach(MIMEText(body, "html"))
s = smtplib.SMTP(server, port)
s.connect(server, port)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtp_user, smtp_password)
s.sendmail(smtp_user, to_address, msg.as_string())
s.quit()