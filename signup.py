import tornado.web
import tornado.websocket
import json
from access_database import *
import hashlib
from login import Authenticated
import re

class SignupHandler(Authenticated):

	def get(self):
		if(self.get_current_user()!=False):
			log_user(self.get_current_user()['id'],f'signup {self.get_argument("next","/home")} get')
			self.redirect(self.get_argument("next","/home"))
		else:
			next_arg = self.get_argument("next",None)
			log_user(-1,f'signup {next_arg} get')
			self.render("signup.html",next_arg=next_arg)
		
	def post(self):
		#if self.get_body_argument('password1') != self.get_body_argument('password2'):
		#    self.render("signup.html",alert="passwords do not match")
		#    return
		
		next_arg = self.get_argument("next",None)
		
		if not bool(re.match("[a-zA-Z0-9._]{4,}$",self.get_body_argument('username'))):
			self.render("signup.html",next_arg=next_arg,alert="invalid username")
			return
		
		user = create_user(username=self.get_body_argument('username'),
					password=hashlib.md5(self.get_body_argument('password1').encode('utf-8')).hexdigest(),
					name=self.get_body_argument('name'),
					email=self.get_body_argument('email'))
		if user is None:
			self.render("signup.html",next_arg=next_arg,alert="username already exists")
			log_user(-1,f'signup {self.get_body_argument("username")} username already exists post')
			return
		self.set_secure_cookie("username",user['username'])
		self.set_secure_cookie("id",str(user['id']))
		self.redirect(self.get_argument("next","/home"))
		log_user(user['id'],f'signup {self.get_argument("next","/home")} post')
