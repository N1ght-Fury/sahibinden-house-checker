import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time

def send_mail(mail,text):
    
    while True:
        try:
            message = MIMEMultipart()
            message["From"] = "Sahibinden Ev İlanları"
            message["To"] = mail
            message["Subject"] = "İstanbul Yeni Ev İlanı"
            message_text = text

            message_content = MIMEText(message_text, "html")
            message.attach(message_content)
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("mail", "pass")
            mail.sendmail(message["From"], message["To"], message.as_string())
            mail.close()
            break

        except Exception as e:
            print(e)
            sys.stderr.write("Something unexpected happend!")
            sys.stderr.flush()
            time.sleep(15)
            continue