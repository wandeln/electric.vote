import tornado.web
from access_database import *
from login import Authenticated

class ChoiceHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,choiceId):
		poll = get_poll_by_choice(choiceId)
		group = get_group_by_poll(poll['id'])
		if not is_group_member(self.current_user['id'],group['id']):
			self.redirect("/home")
			log_user(self.current_user['id'],f'choice id {choiceId} unauthorized get')
			return
		choice = get_choice(self.current_user['id'],choiceId)
		members = get_group_members(self.current_user['id'],group['id'])
		user = get_user(self.current_user['id'])
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		comments = add_tags_to_comments(get_comments_of_choice(choice['id']),exclude=["group","poll","choice"])
		details = get_evaluation_details(choiceId)
		log_user(self.current_user['id'],f'choice id {choiceId} get')
		self.render("choice.html",poll=poll,group=group,choice=choice,members=members,user=user,is_admin=is_admin,comments=comments,details=details)

class ChoiceCreateHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		if not is_group_member(self.current_user['id'],group['id']) or poll['phase']!=0:
			self.redirect("/home")
			log_user(self.current_user['id'],f'choice create poll id {pollId} unauthorized get')
			return
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		if not (is_admin or poll['authorId']==self.current_user['id'] or poll['choiceCreatorLevel']==1):
			self.redirect(f"/poll/{pollId}")
			log_user(self.current_user['id'],f'choice create poll id {pollId} unauthorized get')
			return
		log_user(self.current_user['id'],f'choice create poll id {pollId} get')
		self.render("choice_create.html",pollId=pollId)

	@tornado.web.authenticated
	def post(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		if not is_group_member(self.current_user['id'],group['id']) or poll['phase']!=0:
			self.redirect("/home")
			log_user(self.current_user['id'],f'choice create poll id {pollId} unauthorized post')
			return
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		if not (is_admin or poll['authorId']==self.current_user['id'] or poll['choiceCreatorLevel']==1):
			self.redirect(f"/poll/{pollId}")
			log_user(self.current_user['id'],f'choice create poll id {pollId} unauthorized post')
			return
		
		icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/choices",default="icons/choice")
		log_user(self.current_user['id'],f'choice create poll id {pollId} post')
		choice = create_choice(userId=self.current_user['id'],pollId=pollId,title=self.get_body_argument('title'),description=self.get_body_argument('description'),icon=icon)
		self.redirect(f"/poll/{pollId}")

class ChoiceVoteAjaxHandler(Authenticated):
    
	@tornado.web.authenticated
	def post(self):
		dic = tornado.escape.json_decode(self.request.body)
		choiceId = dic['choiceId']
		poll = get_poll_by_choice(choiceId)
		vote = float(dic['vote'])
		if vote>1:
			vote=1
		elif vote<-1:
			vote=-1
		poll = get_poll_by_choice(choiceId)
		group = get_group_by_poll(poll['id'])
		if is_group_member(self.current_user['id'],group['id']) and poll['phase']<2:
			set_vote(self.current_user['id'],choiceId,vote)
			choices = get_choices(self.current_user['id'],poll['id'])
			data = self.render_string("choices_update.html",choices=choices,poll=poll)
			self.write(data)
			log_user(self.current_user['id'],f'choice id {choiceId} vote ajax post')
		else:
			self.write("error")
			log_user(self.current_user['id'],f'choice id {choiceId} vote ajax unauthorized error post')

class ChoiceVoteDeleteHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,choiceId,redirect):
		poll = get_poll_by_choice(choiceId)
		if poll['phase'] < 2:
			delete_vote(self.current_user['id'],choiceId)
			log_user(self.current_user['id'],f'choice id {choiceId} vote delete get')
		if redirect == "poll":
			self.redirect(f"/poll/{poll['id']}")
		else:
			self.redirect(f"/choice/{choiceId}")

class ChoiceDeleteHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,choiceId):
		poll = get_poll_by_choice(choiceId)
		user = get_user(self.current_user['id'])
		group = get_group_by_poll(poll['id'])
		if is_group_admin(self.current_user['id'],group['id']) or poll['authorId'] == user['id']:
			delete_choice(choiceId)
			log_user(self.current_user['id'],f'choice id {choiceId} delete get')
		else:
			log_user(self.current_user['id'],f'choice id {choiceId} delete unauthorized get')
		self.redirect(f"/poll/{poll['id']}")

class ChoiceSettingsHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,choiceId):
		choice = get_choice(self.current_user['id'],choiceId)
		poll = get_poll_by_choice(choiceId)
		user = get_user(self.current_user['id'])
		if choice['authorId'] != user['id'] or poll['phase']!=0:
			self.redirect("/home")
			log_user(self.current_user['id'],f'choice id {choiceId} settings unauthorized get')
			return
		choice = get_choice(self.current_user['id'],choiceId)
		log_user(self.current_user['id'],f'choice id {choiceId} settings get')
		self.render("choice_settings.html",choice=choice)

	@tornado.web.authenticated
	def post(self,choiceId):
		choice = get_choice(self.current_user['id'],choiceId)
		user = get_user(self.current_user['id'])
		poll = get_poll_by_choice(choiceId)
		if choice['authorId'] == user['id'] and poll['phase']==0:
			title = self.get_body_argument('title')
			if title == "":
				title = None
			description = self.get_body_argument('description')
			if description == "":
				description = None
			
			icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/choices",default=None)
		
			choice = update_choice(self.current_user['id'],choiceId,title=title,description=description,icon=icon)
			log_user(self.current_user['id'],f'choice id {choiceId} settings post')
		else:
			log_user(self.current_user['id'],f'choice id {choiceId} settings unauthorized post')
		self.redirect(f"/choice/{choiceId}")
