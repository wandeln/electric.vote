import tornado.web
import tornado.websocket
import json
import threading
import sys
import asyncio
from access_database import *
from login import Authenticated

class HomeHandler(Authenticated):

	@tornado.web.authenticated
	def get(self):
		log_user(self.current_user['id'],'home get')
		user = get_user(self.current_user['id'])
		groups = get_groups(self.current_user['id'])
		polls = get_polls_of_user(self.current_user['id'],phase=[0,1,2])
		self.render("home.html",user=user,groups=groups,polls=polls)

class HomeAjaxHandler(Authenticated):

	@tornado.web.authenticated
	def post(self):
		dic = tornado.escape.json_decode(self.request.body)
		phase = []
		if dic['open']:
			phase.append(0)
		if dic['voting']:
			phase.append(1)
		if dic['closed']:
			phase.append(2)
		log_user(self.current_user['id'],f'home filter {phase} ajax post')
		polls = get_polls_of_user(self.current_user['id'],phase=phase)
		data = self.render_string("polls_update.html",polls=polls)
		self.write(data)

class LegalHandler(Authenticated):

	def get(self,target):
		current_user = self.get_current_user()
		userId = -1
		if current_user:
			user = get_user(current_user['id'])
			userId = self.current_user['id']
		else:
			user = None
		if target == "imprint":
			log_user(userId,'legal imprint get')
			self.render("legal/imprint.html",user=user)
		if target == "donation":
			log_user(userId,'legal donation get')
			self.render("legal/donate.html",user=user)
		if target == "terms_of_use":
			log_user(userId,'legal terms_of_use get')
			self.render("legal/terms_of_use.html",user=user)
