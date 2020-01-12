import tornado.web
from access_database import *
from login import Authenticated
from utils import randomString
from send_email import send_group_email
from tornado.escape import linkify

n_max_members = 256

class GroupHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_member(self.current_user['id'],groupId):
			log_user(self.current_user['id'],f'group id {groupId} unauthorized get')
			self.redirect("/home")
			return
		log_user(self.current_user['id'],f'group id {groupId} get')
		user = get_user(self.current_user['id'])
		group = get_group(groupId)
		members = get_group_members(self.current_user['id'],groupId)
		n_group_admins = get_n_group_admins(groupId)
		polls = get_polls(groupId,phase=[0,1,2])
		is_admin = is_group_admin(self.current_user['id'],groupId)
		comments = add_tags_to_comments(get_comments_of_group(groupId),exclude=["group"])
		self.render("group.html",group=group,polls=polls,members=members,is_admin=is_admin,comments=comments,user=user,n_group_admins=n_group_admins)

class GroupCreateHandler(Authenticated):

	@tornado.web.authenticated
	def get(self):
		log_user(self.current_user['id'],'group create get')
		self.render("group_create.html")

	@tornado.web.authenticated
	def post(self):
		try:
			pollCreatorLevel = 1 if self.get_body_argument('mccp') else 2
		except:
			pollCreatorLevel = 2
		
		icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/groups",default="icons/group")
		
		group = create_group(userId=self.current_user['id'],name=self.get_body_argument('name'),
								motto=self.get_body_argument('motto'),description=self.get_body_argument('description'),pollCreatorLevel=pollCreatorLevel,icon=icon)
		
		self.redirect(f"/group/{group['id']}")
		
		log_user(self.current_user['id'],f'group id {group["id"]} {pollCreatorLevel} create post')

class GroupAddMemberHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'group id {groupId} unauthorized add member post')
			return
		group = get_group(groupId)
		n_members = len(get_group_members(self.current_user['id'],groupId))+1
		members = get_group_member_suggestions(self.current_user['id'],groupId)
		self.render("group_add_member.html",group=group,members=members,n_members=n_members,n_max_members=n_max_members)
		log_user(self.current_user['id'],f'group id {groupId} {n_members} add member post')

	@tornado.web.authenticated
	def post(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			user = get_user_by_username(self.get_body_argument("username"))
			n_members = len(get_group_members(self.current_user['id'],groupId))+1
			if n_members >= n_max_members:
				group = get_group(groupId)
				self.render("group_add_member.html",group=group,alert="too many members")
				return
			if user is not None and not is_group_member(user['id'],groupId):
				group_add_member(userId=user['id'],groupId=groupId,granterId=self.current_user['id'])
		self.redirect(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} add member post')

class GroupAddMemberAjaxHandler(Authenticated):

	@tornado.web.authenticated
	def post(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.write("/home")
			return
		
		dic = tornado.escape.json_decode(self.request.body)
		n_members = len(get_group_members(self.current_user['id'],groupId))+1
		if n_members + len(dic['members'])>n_max_members:
			self.write(f"/group_add_member/{groupId}")
			return
		for username in dic['members']:
			user = get_user_by_username(username)
			if user is not None and not is_group_member(user['id'],groupId):
				group_add_member(userId=user['id'],groupId=groupId,granterId=self.current_user['id'])
		self.write(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} add member ajax post')

class GroupAddMemberSuggestionsHandler(Authenticated):

	@tornado.web.authenticated
	def post(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.write("error")
			return
		
		dic = tornado.escape.json_decode(self.request.body)
		members = get_group_member_suggestions(self.current_user['id'],groupId,name=dic['name'])
		data = self.render_string("users_update.html",members=members)
		self.write(data)

class GroupRemoveMemberHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			return
		group = get_group(groupId)
		members = get_group_members(self.current_user['id'],groupId)
		user = get_user(self.current_user['id'])
		self.render("group_remove_member.html",user=user,group=group,members=members)
		log_user(self.current_user['id'],f'group id {groupId} remove member get')

	@tornado.web.authenticated
	def post(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.write("/home")
			return
		dic = tornado.escape.json_decode(self.request.body)
		for username in dic['members']:
			user = get_user_by_username(username)
			if not is_group_admin(user['id'],groupId):
				group_remove_member(userId=user['id'],groupId=groupId)
		self.write(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} {len(dic["members"])} remove member post')

class GroupMakeAdminHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			return
		group = get_group(groupId)
		members = get_group_members(self.current_user['id'],groupId)
		self.render("group_make_admin.html",group=group,users=members)
		log_user(self.current_user['id'],f'group id {groupId} make admin get')

	@tornado.web.authenticated
	def post(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.write("/home")
			return
		dic = tornado.escape.json_decode(self.request.body)
		for username in dic['members']:
			user = get_user_by_username(username)
			group_make_admin(userId=user['id'],groupId=groupId,granterId=self.current_user['id'])
		self.write(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} {len(dic["members"])} make admin post')

class GroupDeleteHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_admin(self.current_user['id'],groupId) and get_n_group_admins(groupId) <= 1:
			delete_group(groupId)
		self.redirect(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} delete get')

class GroupLeaveHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_member(self.current_user['id'],groupId):
			leave_group(self.current_user['id'],groupId)
		self.redirect("/home")
		log_user(self.current_user['id'],f'group id {groupId} leave get')

class GroupInvitationHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId,key):
		if is_group_member(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			return
		alert = None
		group = get_group(groupId)
		if key != group["invitationKey"]:
			alert = "wrong invitation link"
		n_members = len(get_group_members(self.current_user['id'],groupId))
		if n_members >= n_max_members:
			alert = "maximum number of members already reached"
		if alert is not None:
			user = get_user(self.current_user['id'])
			groups = get_groups(self.current_user['id'])
			polls = get_polls_of_user(self.current_user['id'],phase=[0,1,2])
			self.render("home.html",user=user,groups=groups,polls=polls,alert=alert)
			return
		group_add_member(userId=self.current_user['id'],groupId=groupId,granterId=group['authorId'])
		self.redirect(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} invitation get')
		return

class GroupInvitationSettingsHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			group = get_group(groupId)
			link = ""
			if group["invitationKey"]:
				link = f"https://electric.vote/group_invitation/{groupId}/{group['invitationKey']}"
			self.render("group_invitation.html",group=group,link=link)
			log_user(self.current_user['id'],f'group id {groupId} invitation settings get')
			return
		self.redirect(f"/group/{groupId}")
		log_user(self.current_user['id'],f'group id {groupId} invitation settings unauthorized get')

class GroupNewInvitationKeyHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			update_group(groupId,invitationKey=randomString(10))
			log_user(self.current_user['id'],f'group id {groupId} new invitation key get')
		else:
			log_user(self.current_user['id'],f'group id {groupId} new invitation key unauthorized get')
		self.redirect(f"/group_invitation_settings/{groupId}")

class GroupResetInvitationKeyHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			reset_group_invitation_key(groupId)
			log_user(self.current_user['id'],f'group id {groupId} reset invitation key get')
		else:
			log_user(self.current_user['id'],f'group id {groupId} reset invitation key unauthorized get')
		self.redirect(f"/group_invitation_settings/{groupId}")

class GroupResignHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			resign_group(self.current_user['id'],groupId)
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'group id {groupId} resign get')
		else:
			log_user(self.current_user['id'],f'group id {groupId} resign unauthorized get')
		self.redirect("/home")

class GroupSettingsHandler(Authenticated):
    
	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'group id {groupId} settings unauthorized get')
			return
		group = get_group(groupId)
		self.render("group_settings.html",group=group)
		log_user(self.current_user['id'],f'group id {groupId} settings get')

	@tornado.web.authenticated
	def post(self,groupId):
		if is_group_admin(self.current_user['id'],groupId):
			name = self.get_body_argument('name')
			if name == "":
				name = None
			
			motto = self.get_body_argument('motto')
			if motto == "":
				motto = None
			
			description = self.get_body_argument('description')
			if description == "":
				description = None
			
			icon = save_image(request=self.request,file_object="picture",username=self.current_user["username"],folder="images/groups",default=None)
		
			try:
				pollCreatorLevel = 1 if self.get_body_argument('mccp') else 2
			except:
				pollCreatorLevel = 2
			group = update_group(groupId,name=name,motto=motto,description=description,pollCreatorLevel=pollCreatorLevel,icon=icon)
			log_user(self.current_user['id'],f'group id {groupId} settings post')
		else:
			log_user(self.current_user['id'],f'group id {groupId} settings unauthorized post')
		self.redirect(f"/group/{group['id']}")

class GroupSendCircularHandler(Authenticated):

	@tornado.web.authenticated
	def get(self,groupId):
		if not is_group_admin(self.current_user['id'],groupId):
			self.redirect(f"/group/{groupId}")
			log_user(self.current_user['id'],f'group id {groupId} send circular unauthorized get')
			return
		group = get_group(groupId)
		self.render("group_send_circular.html",group=group)
		log_user(self.current_user['id'],f'group id {groupId} send circular get')

	@tornado.web.authenticated
	def post(self,groupId):
		group = get_group(groupId)
		if is_group_admin(self.current_user['id'],groupId):
			content = self.get_body_argument('content')
			user = get_user(self.current_user['id'])
			subject = f"{group['name']} ({self.translate()('Circular')})"
			text = f"{group['name']}\n\n{user['name']}:\n{content}"
			html = self.render_string("circular_mail.html",group=group,user=user,content=esc_m(content)).decode('utf-8')
			send_group_email(group,subject=subject,text=text,html=html)
			log_user(self.current_user['id'],f'group id {groupId} send circular post')
		else:
			log_user(self.current_user['id'],f'group id {groupId} send circular unauthorized post')
		self.redirect(f"/group/{group['id']}")

class GroupAjaxHandler(Authenticated):

	@tornado.web.authenticated
	def post(self,groupId):
		if is_group_member(self.current_user['id'],groupId):
			dic = tornado.escape.json_decode(self.request.body)
			phase = []
			if dic['open']:
				phase.append(0)
			if dic['voting']:
				phase.append(1)
			if dic['closed']:
				phase.append(2)
			polls = get_polls(groupId,phase=phase)
			data = self.render_string("polls_update.html",polls=polls)
			self.write(data)
			log_user(self.current_user['id'],f'group id {groupId} filter {phase} ajax post')
		else:
			log_user(self.current_user['id'],f'group id filter ajax unauthorized post')
			self.write("error")
