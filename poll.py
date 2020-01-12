import tornado.web
from access_database import *
from login import Authenticated
from send_email import send_group_email

class PollHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,pollId):
		group = get_group_by_poll(pollId)
		
		if group is None:
			self.redirect("/home")
			log_user(self.current_user['id'],f'poll id {pollId} does not exist get')
			return
		
		if not is_group_member(self.current_user['id'],group['id']):
			self.redirect("/home")
			log_user(self.current_user['id'],f'poll id {pollId} unauthorized get')
			return
		members = get_group_members(self.current_user['id'],group['id'])
		user = get_user(self.current_user['id'])
		poll = get_poll(pollId)
		choices = get_choices(self.current_user['id'],pollId)
		comments = add_tags_to_comments(get_comments_of_poll(pollId),exclude=["group","poll"])
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		evaluation = get_all_evaluations(pollId)
		log_user(self.current_user['id'],f'poll id {pollId} get')
		self.render("poll.html",poll=poll,group=group,choices=choices,members=members,user=user,is_admin=is_admin,evaluation=evaluation,comments=comments)

class PollCreateHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_member(self.current_user['id'],groupId):
			self.redirect("/home")
			log_user(self.current_user['id'],f'poll id {groupId} create unauthorized get')
			return
		group = get_group(groupId)
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		if not (is_admin or group['authorId']==self.current_user['id'] or group['pollCreatorLevel']==1):
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'poll id {groupId} create unauthorized get')
			return
		log_user(self.current_user['id'],f'poll id {groupId} create get')
		self.render("poll_create.html",groupId=groupId)

	@tornado.web.authenticated
	def post(self,groupId):
		if not is_group_member(self.current_user['id'],groupId):
			self.redirect("/home")
			log_user(self.current_user['id'],f'poll id {groupId} create unauthorized post')
			return
		group = get_group(groupId)
		is_admin = is_group_admin(self.current_user['id'],group['id'])
		if not (is_admin or group['authorId']==self.current_user['id'] or group['pollCreatorLevel']==1):
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'poll id {groupId} create unauthorized post')
			return
		
		icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/polls",default="icons/poll")
		
		try:
			secret = self.get_body_argument('secret')
		except:
			secret = False
		try:
			choiceCreatorLevel = 1 if self.get_body_argument('mccc') else 2
		except:
			choiceCreatorLevel = 2
		poll = create_poll(userId=self.current_user['id'],groupId=groupId,title=self.get_body_argument('title'),description=self.get_body_argument('description'),secret=secret,choiceCreatorLevel=choiceCreatorLevel,icon=icon)
		self.redirect(f"/poll/{poll['id']}")
		log_user(self.current_user['id'],f'poll id {poll["id"]} create post')

class PollEvaluateHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		if not is_group_member(self.current_user['id'],group['id']):
			self.redirect("/home")
			return
		if is_group_admin(self.current_user['id'],group['id']) or poll['authorId'] == self.current_user['id']:
			if poll['phase']<2:
				evaluate_poll(self.current_user['id'],pollId)
				
		self.redirect(f"/poll/{pollId}")
		log_user(self.current_user['id'],f'poll id {pollId} evaluate get')

class PollDeleteHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		user = get_user(self.current_user['id'])
		if is_group_admin(self.current_user['id'],group['id']) or poll['authorId'] == user['id']:
			delete_poll(pollId)
			log_user(self.current_user['id'],f'poll id {pollId} delete get')
		else:
			log_user(self.current_user['id'],f'poll id {pollId} delete unauthorized get')
		self.redirect(f"/group/{group['id']}")

class PollSettingsHandler(Authenticated):
	
	@tornado.web.authenticated
	def get(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		user = get_user(self.current_user['id'])
		if poll['authorId'] != user['id'] or poll['phase']!=0:
			self.redirect("/home")
			log_user(self.current_user['id'],f'poll id {pollId} settings unauthorized get')
			return
		self.render("poll_settings.html",poll=poll)
		log_user(self.current_user['id'],f'poll id {pollId} settings get')

	@tornado.web.authenticated
	def post(self,pollId):
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		user = get_user(self.current_user['id'])
		if poll['authorId'] == user['id'] and poll['phase']==0:
			title = self.get_body_argument('title')
			if title == "":
				title = None
			description = self.get_body_argument('description')
			if description == "":
				description = None
			
			icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/polls",default=None)
		
			try:
				choiceCreatorLevel = 1 if self.get_body_argument('mccc') else 2
			except:
				choiceCreatorLevel = 2
			poll = update_poll(pollId,title=title,description=description,icon=icon,choiceCreatorLevel=choiceCreatorLevel)
			log_user(self.current_user['id'],f'poll id {pollId} settings post')
		else:
			log_user(self.current_user['id'],f'poll id {pollId} settings unauthorized post')
		self.redirect(f"/poll/{pollId}")

class PollSetPhaseHandler(Authenticated):
	#poll phases: 
	# 0: choice definition phase (choices can be created/changed and preliminary votes can be made)
	# 1: voting phase (choices are freezed and votes can be made)
	# 2: closed (choices and votes are freezed, results can be discussed...)
	
	@tornado.web.authenticated
	def get(self,pollId,phase):
		phase = int(phase)
		group = get_group_by_poll(pollId)
		poll = get_poll(pollId)
		user = get_user(self.current_user['id'])
		if is_group_admin(self.current_user['id'],group['id']) or poll['authorId'] == user['id']:
			if poll['phase']==0 and phase==1:
				update_poll(pollId,phase=1)
			if poll['phase']==1 and phase==2:
				update_poll(pollId,phase=2)
			if phase == 2:
				evaluate_poll(self.current_user['id'],pollId)
				
				results = get_latest_evaluation(pollId)
				results_txt = '\n'.join([f"{r['proposal']['title_unesc']}: {round(r['result'],3)}" for r in results["results"]])
				subject = f"{poll['title']} ({self.translate()('Result')})"
				text = f"{poll['title_unesc']}\n\n{poll['description_unesc']}\n\n{self.translate()('Result')}:\n{results_txt}"
				html = self.render_string("result_mail.html",group=group,poll=poll,results=results).decode('utf-8')
				send_group_email(group,subject=subject,text=text,html=html)
				
			log_user(self.current_user['id'],f'poll id {pollId} set phase {phase} get')
		else:
			log_user(self.current_user['id'],f'poll id {pollId} set phase {phase} unauthorized get')
		self.redirect(f"/poll/{pollId}")
