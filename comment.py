import tornado.web
from access_database import *
from login import Authenticated

class CommentHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,commentId):
		comment = get_comment(commentId)
		if not is_group_member(self.current_user['id'],comment['groupId']):
			self.redirect("/home")
			log_user(self.current_user['id'],f'comment id {commentId} unauthorized get')
			return
		user = get_user(self.current_user['id'])
		comment["tags"] = get_comment_tags(commentId)
		members = get_group_members(self.current_user['id'],comment['groupId'])
		comments = get_comments_of_comment(commentId)
		group = get_group(comment['groupId'])
		log_user(self.current_user['id'],f'comment id {commentId} get')
		self.render("comment.html",comment=comment,user=user,comments=comments,members=members,group=group)

class CommentCreateHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,origin,ID):
		log_user(self.current_user['id'],f'comment create origin {origin} id {ID} get')
		if origin == "choice":
			group = get_group_by_choice(ID)
			if not is_group_member(self.current_user['id'],group['id']):
				self.redirect("/home")
				return
			self.render("comment_create.html",origin=origin,ID=ID)
			return
		if origin == "poll":
			group = get_group_by_poll(ID)
			if not is_group_member(self.current_user['id'],group['id']):
				self.redirect("/home")
				return
			self.render("comment_create.html",origin=origin,ID=ID)
			return
		if origin == "group":
			group = get_group(ID)
			if not is_group_member(self.current_user['id'],group['id']):
				self.redirect("/home")
				return
			self.render("comment_create.html",origin=origin,ID=ID)
			return
		if origin == "comment":
			self.render("comment_create.html",origin=origin,ID=ID)
			return
		self.redirect("/home")

	@tornado.web.authenticated
	def post(self,origin,ID):
		log_user(self.current_user['id'],f'comment create origin {origin} id {ID} post')
		if origin == "choice":
			group = get_group_by_choice(ID)
			if not is_group_member(self.current_user['id'],group['id']):
				self.redirect("/home")
				return
			poll = get_poll_by_choice(ID)
			comment = create_comment(userId=self.current_user['id'],content=self.get_body_argument('content'),groupId=group['id'])
			tag_comment_poll(comment['id'],poll['id'])
			tag_comment_choice(comment['id'],ID)
			self.redirect(f"/choice/{ID}")
			return
		if origin == "poll":
			group = get_group_by_poll(ID)
			if not is_group_member(self.current_user['id'],group['id']):
				self.redirect("/home")
				return
			poll = get_poll(ID)
			comment = create_comment(userId=self.current_user['id'],content=self.get_body_argument('content'),groupId=group['id'])
			tag_comment_poll(comment['id'],poll['id'])
			self.redirect(f"/poll/{ID}")
			return
		if origin == "group":
			if not is_group_member(self.current_user['id'],ID):
				self.redirect("/home")
				return
			comment = create_comment(userId=self.current_user['id'],content=self.get_body_argument('content'),groupId = ID)
			self.redirect(f"/group/{ID}")
			return
		if origin == "comment":
			commented_comment = get_comment(ID)
			if not is_group_member(self.current_user['id'],commented_comment['groupId']):
				self.redirect("/home")
				return
			comment = create_comment(userId=self.current_user['id'],content=self.get_body_argument('content'),groupId=commented_comment['groupId'])
			tag_comment_comment(comment['id'],ID)
			self.redirect(f"/comment/{ID}")
			return
		self.redirect("/home")

class CommentDeleteHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,commentId):
		comment = get_comment(commentId)
		user = get_user(self.current_user['id'])
		if comment['authorId'] == user['id']:
			delete_comment(commentId)
			log_user(self.current_user['id'],f'comment id {commentId} delete get')
		else:
			log_user(self.current_user['id'],f'comment id {commentId} delete unauthorized get')
		self.redirect("/home")
