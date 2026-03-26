import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

date = datetime.datetime.now().date()
smtp_server = "smtp.gmail.com"
smtp_port = 587
email = "hinke71@gmail.com"
sender_password = "amkn krcs yhdv nskp"

msg = MIMEMultipart()
msg["From"] = email
msg["To"] = email
msg["Subject"] = f"Rapport - {date}"

def send(body=""):
    try:
        msg.attach(MIMEText(body, "plain"))
        print("Trying to connect...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("Server declered")
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(email, sender_password)
        print("Connected")

        server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        server.quit()