import tornado.web

class ModuleTileGroup(tornado.web.UIModule):
	def render(self, group):
		return self.render_string("module_tile_group.html",group=group)

class ModuleTileProfile(tornado.web.UIModule):
	def render(self, user):
		return self.render_string("module_tile_profile.html",user=user)

class ModuleTileUser(tornado.web.UIModule):
	def render(self, user):
		return self.render_string("module_tile_user.html",user=user)

class ModuleTileMember(tornado.web.UIModule):
	def render(self, member, group):
		return self.render_string("module_tile_member.html",member=member,group=group)

class ModuleTilePoll(tornado.web.UIModule):
	def render(self, poll):
		return self.render_string("module_tile_poll.html",poll=poll)

class ModuleTileChoice(tornado.web.UIModule):
	def render(self, choice, poll):
		return self.render_string("module_tile_choice.html",choice=choice,poll=poll)

class ModuleTileComment(tornado.web.UIModule):
	def render(self, comment):
		return self.render_string("module_tile_comment.html",comment=comment)
