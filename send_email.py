import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import Certificates.passwords as pw
from access_database import *

sender_email = "info@electric.vote"
password = pw.email_password


def send_email(user,subject,text,html):
	if user["email"] != "":
		message = MIMEMultipart("alternative")
		message["subject"] = subject
		message["From"] = "info@electric.vote"
		message["To"] = user["email"]
		message.attach(MIMEText(text,"plain"))
		if html is not None:
			message.attach(MIMEText(html,"html"))
		
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("mail.privateemail.com",465,context = context) as server:
			server.login(sender_email,password)
			server.sendmail(sender_email,user['email'],message.as_string())

def send_group_email(group,subject,text,html):
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("mail.privateemail.com",465,context = context) as server:
		server.login(sender_email,password)
		
		for user in get_group_users(group["id"]):
			if user["email"] != "":
				message = MIMEMultipart("alternative")
				message["subject"] = subject
				message["From"] = "info@electric.vote"
				message["To"] = user["email"]
				message.attach(MIMEText(text,"plain"))
				if html is not None:
					message.attach(MIMEText(html,"html"))
				server.sendmail(sender_email,user['email'],message.as_string())
