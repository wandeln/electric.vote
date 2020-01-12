import tornado.web
import tornado.websocket
import json
import random
from access_database import *
from send_email import send_email
import hashlib
from utils import randomString
from translate import Translated

class Authenticated(Translated):
	def get_current_user(self):
		username = self.get_secure_cookie("username")
		userId = self.get_secure_cookie("id")
		if username is None or userId is None:
			return False
		return {"username":str(username)[2:-1],"id":str(userId)[2:-1]}

class LogoutHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self):
		log_user(self.current_user['id'],'logout get')
		self.clear_cookie("username")
		self.clear_cookie("id")
		self.redirect("/login")

class LoginHandler(Authenticated):
	
	def get(self):
		if self.get_current_user()!=False:
			log_user(self.get_current_user()['id'],'login get')
			self.redirect(self.get_argument("next","/home"))
		else:
			log_user(-1,'login get')
			next_arg = self.get_argument("next",None)
			self.render("login.html",next_arg=next_arg)
			
	def post(self):
		user = get_user_by_username(self.get_body_argument('username'))
		next_arg = self.get_argument("next",None)
		if user is None:
			log_user(-1,'login wrong username post')
			self.render("login.html",next_arg=next_arg,alert="username incorrect")
			return
		elif user['password'] != hashlib.md5(self.get_body_argument('password').encode('utf-8')).hexdigest():
			log_user(-1,'login wrong password post')
			self.render("login.html",next_arg=next_arg,alert="password incorrect")
		else:
			log_user(user['id'],'login correct post')
			self.set_secure_cookie("username",str(user['username']))
			self.set_secure_cookie("id",str(user['id']))
			self.redirect(self.get_argument("next","/home"))

class ResetPasswordHandler(Translated):

	def get(self):
		log_user(-1,'reset password get')
		self.render("reset_password.html")

	def post(self):
		user = get_user_by_username(self.get_body_argument('username'))
		if user is None:
			log_user(-1,'reset password wrong username post')
			self.render("reset_password.html",alert="username incorrect. If you do not know your username anymore, pease write us an email (info@electric.vote)")
			return
		else:
			log_user(user['id'],'reset password correct post')
			user = update_user(user['id'],reset_key=randomString(10))
			resetLink = f"https://electric.vote/new_password/{user['username']}/{user['reset_key']}"
			send_email(user,"new password",f"Dear {user['name']},\nyou can set a new password using the following link: {resetLink}.\nIf you didn't request a password reset, this email can be savely ignored.\nKind regards,\nNils Wandel",f"<html><body>Dear {user['name']},<br><br>you can set a new password <a href='{resetLink}'>here</a>.<br>If you didn't request a password reset, this email can be savely ignored.<br><br>Kind regards,<br>Nils Wandel</body></html>")
			self.render("login.html",alert="We are sending you an email to reset your password. This may take a few minutes. Be sure to check your junk inbox as well. If you are still facing problems: please write us an email (info@electric.vote)")

class NewPasswordHandler(Translated):
	
	def get(self,username,reset_key):
		user = get_user_by_username(username)
		if user is None:
			log_user(-1,'new password wrong username get')
			self.render("reset_password.html",alert="invalid password reset link")
			return
		if reset_key != user['reset_key']:
			log_user(-1,'new password wrong reset key get')
			self.render("reset_password.html",alert="invalid or expired password reset link")
			return
		log_user(-1,'new password get')
		self.render("new_password.html",user=user)

	def post(self,username,reset_key):
		user = get_user_by_username(username)
		if user is None:
			log_user(-1,'new password wrong username post')
			self.redirect("reset_password.html")
			return
		if reset_key != user['reset_key']:
			log_user(-1,'new password wrong reset key post')
			self.redirect("reset_password.html")
			return
		password = self.get_body_argument('password')
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		update_user(user['id'],password=password)
		reset_user_reset_key(user['id'])
		self.set_secure_cookie("username",str(user['username']))
		self.set_secure_cookie("id",str(user['id']))
		self.redirect("/home")
