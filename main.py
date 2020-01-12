import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.websocket
from tornado.options import define, options
from utils import is_mobile
import modules
import signup
import login
import home
import group
import poll
import choice
import comment
import user
import translate
from Certificates.passwords import cookie_secret

class HTTPRedirectHandler(tornado.web.RequestHandler):
	def get(self,address):
		self.redirect(f"https://electric.vote{address}")

class My404Handler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
	def get(self):
		self.write("Ups... page not found")

def make_app(debug = False):
	settings = dict(
		static_path="static",
		template_path="template",
		include_version=False,
		cookie_secret=cookie_secret,
		xsrf_cookies=True,
		debug=debug,
		login_url="/login")
	return tornado.web.Application(
		[("/", signup.SignupHandler),
			("/signup", signup.SignupHandler),
			("/login", login.LoginHandler),
			("/logout", login.LogoutHandler),
			("/reset_password", login.ResetPasswordHandler),
			("/new_password/(.*)/(.*)", login.NewPasswordHandler),
			("/change_language", translate.ChangeLanguageHandler),
			("/home", home.HomeHandler),
			("/home_ajax", home.HomeAjaxHandler),
			("/legal/(.*)", home.LegalHandler),
			("/group/(.*)", group.GroupHandler),
			("/group_create", group.GroupCreateHandler),
			("/group_add_member/(.*)", group.GroupAddMemberHandler),
			("/group_add_member_ajax/(.*)", group.GroupAddMemberAjaxHandler),
			("/group_add_member_suggestions/(.*)", group.GroupAddMemberSuggestionsHandler),
			("/group_remove_member/(.*)", group.GroupRemoveMemberHandler),
			("/group_make_admin/(.*)", group.GroupMakeAdminHandler),
			("/group_delete/(.*)", group.GroupDeleteHandler),
			("/group_leave/(.*)", group.GroupLeaveHandler),
			("/group_invitation/(.*)/(.*)", group.GroupInvitationHandler),
			("/group_invitation_settings/(.*)", group.GroupInvitationSettingsHandler),
			("/group_new_invitation_key/(.*)", group.GroupNewInvitationKeyHandler),
			("/group_reset_invitation_key/(.*)", group.GroupResetInvitationKeyHandler),
			("/group_resign/(.*)", group.GroupResignHandler),
			("/group_settings/(.*)", group.GroupSettingsHandler),
			("/group_send_circular/(.*)", group.GroupSendCircularHandler),
			("/group_ajax/(.*)", group.GroupAjaxHandler),
			("/poll/(.*)", poll.PollHandler),
			("/poll_create/(.*)", poll.PollCreateHandler),
			("/poll_evaluate/(.*)", poll.PollEvaluateHandler),
			("/poll_delete/(.*)", poll.PollDeleteHandler),
			("/poll_settings/(.*)", poll.PollSettingsHandler),
			("/poll_set_phase/(.*)/(.*)", poll.PollSetPhaseHandler),
			("/choice/(.*)", choice.ChoiceHandler),
			("/choice_create/(.*)", choice.ChoiceCreateHandler),
			("/choice_vote_ajax", choice.ChoiceVoteAjaxHandler),
			("/choice_vote_delete/(.*)/(.*)", choice.ChoiceVoteDeleteHandler),
			("/choice_delete/(.*)", choice.ChoiceDeleteHandler),
			("/choice_settings/(.*)", choice.ChoiceSettingsHandler),
			("/comment/(.*)", comment.CommentHandler),
			("/comment_create/(.*)/(.*)", comment.CommentCreateHandler),
			("/comment_delete/(.*)", comment.CommentDeleteHandler),
			("/user/(.*)", user.UserHandler),
			("/user_delete", user.UserDeleteHandler),
			("/user_follow_ajax", user.UserFollowAjaxHandler),
			("/user_search_ajax", user.UserSearchAjaxHandler),
			("/user_settings", user.UserSettingsHandler)],
		ui_modules={'TileGroup':modules.ModuleTileGroup,
					'TileUser':modules.ModuleTileUser,
					'TileProfile':modules.ModuleTileProfile,
					'TileMember':modules.ModuleTileMember,
					'TilePoll':modules.ModuleTilePoll,
					'TileChoice':modules.ModuleTileChoice,
					'TileComment':modules.ModuleTileComment},
		default_handler_class=My404Handler,
		**settings),tornado.web.Application([("(.*)", HTTPRedirectHandler)])

if __name__=="__main__":
	define("https_port", default=443, help="run https server on the given port", type=int)
	define("http_port", default=80, help="run http server on the given port", type=int)
	define("debug", default=False, help="run server in debug mode", type=bool)
	options.parse_command_line()
	HTTPSapp,HTTPapp = make_app(debug = options.debug)
	settings = dict(ssl_options={"certfile":"Certificates/mykey.crt","keyfile":"Certificates/mykey.key"})
	HTTPSserver = tornado.httpserver.HTTPServer(HTTPSapp,**settings)
	HTTPSserver.listen(options.https_port)
	HTTPserver = tornado.httpserver.HTTPServer(HTTPapp)
	HTTPserver.listen(options.http_port)
	tornado.ioloop.IOLoop.instance().start()
