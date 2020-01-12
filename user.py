import tornado.web
from access_database import *
from login import Authenticated
import json
import hashlib

class UserHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,userName):
		user = get_user_by_username(userName)
		if user is None:
			self.redirect("/home")
			return
		user_me = get_user(self.current_user['id'])
		comments = add_tags_to_comments(get_comments_of_author_related_to_user(user['id'],self.current_user['id']))
		groups = get_common_groups(user['id'],self.current_user['id'])
		log_user(self.current_user['id'],f'user name {userName} get')
		self.render("user.html",user_me=user_me,user=user,is_owner=str(user['id'])==self.current_user['id'],comments=comments,groups=groups)

class UserDeleteHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self):
		delete_user(self.current_user['id'])
		self.clear_cookie("username")
		self.clear_cookie("id")
		self.redirect("/signup")
		log_user(self.current_user['id'],f'user delete get')

class UserFollowAjaxHandler(Authenticated):
	
	@tornado.web.authenticated
	def post(self):
		dic = tornado.escape.json_decode(self.request.body)
		weight = float(dic['weight'])
		if weight > 1:
			weight = 1
		if weight < 0:
			weight = 0
		groupId = dic['groupId']
		username = dic['username']
		search = dic['search']
		user = get_user(self.current_user['id'])
		group = get_group(groupId)
		if is_group_member(self.current_user['id'],group['id']):
			user2follow = get_user_by_username(username)
			set_follow(user['id'],user2follow['id'],groupId,weight)
			members = get_group_members(self.current_user['id'],groupId,search)
			group = get_group(groupId)
			data = self.render_string("members_update.html",members=members,group=group)
			self.write(data)
		else:
			self.write("error")

class UserSearchAjaxHandler(Authenticated):
	
	@tornado.web.authenticated
	def post(self):
		dic = tornado.escape.json_decode(self.request.body)
		groupId = dic['groupId']
		search = dic['search']
		user = get_user(self.current_user['id'])
		group = get_group(groupId)
		if is_group_member(self.current_user['id'],group['id']):
			members = get_group_members(self.current_user['id'],groupId,search)
			group = get_group(groupId)
			data = self.render_string("members_update.html",members=members,group=group)
			self.write(data)
		else:
			self.write("error")

class UserSettingsHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self):
		user = get_user(self.current_user['id'])
		log_user(self.current_user['id'],f'user settings get')
		self.render("user_settings.html",user=user)

	@tornado.web.authenticated
	def post(self):
		
		log_user(self.current_user['id'],f'user settings post')
		password = self.get_body_argument('password1')
		if password != self.get_body_argument('password2'):
			user = get_user(self.current_user['id'])
			self.render("user_settings.html",user=user,alert="passwords do not match")
			return
		if password == "":
			password = None
		else:
			password = hashlib.md5(password.encode('utf-8')).hexdigest()
		
		name = self.get_body_argument('name')
		if name == "":
			name = None
		
		description = self.get_body_argument('description')
		if description == "":
			description = None
		
		email = self.get_body_argument('email')
		if email == "":
			email=None
		
		icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/users",default=None)
		
		user = update_user(userId=self.current_user['id'],password=password,name=name,email=email,description=description,icon=icon)
		
		#language = self.get_body_argument('language')
		#self.set_secure_cookie("language",language)
		
		self.redirect(f"/user/{self.current_user['username']}")
