import tornado.web

class Translated(tornado.web.RequestHandler):
	
	def get_language(self):
		if self.get_secure_cookie("language") is None:
			return "en"
		return self.get_secure_cookie("language").decode('utf-8')
	
	def translate(self):
		return translate(self.get_language())
	
	def render_string(self,text,**args):
		return super().render_string(text,**args,translate=self.translate())

def translate(language,key=None):
	if key is not None:
		if language not in languages_dict.keys():
			language = "en"
			#raise Exception("language not supported", language)
		if key not in languages_dict[language].keys():
			return key
		return languages_dict[language][key]
	def t(key):
		return translate(language,key)
	return t

class ChangeLanguageHandler(Translated):

	def post(self):
		
		language = self.get_body_argument('language')
		self.set_secure_cookie("language",language)
		
		self.redirect(f"javascript://")


languages_dict = {
	"en":{
		"language_ID":"en"
		,"welcome login":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 40px">Welcome to electric.vote!</h1>
			<h2>... where communities meet the power of delegative democracy</h2>
			<a href="/reset_password"><h3 style="font-style: italic">- forgot password?</h3></a>
			</div>"""
		,"welcome sign up":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 40px">Welcome to electric.vote!</h1>
			<!--h2>... where communities meet the power of delegative democracy</h2-->
			<h2>make voting:</h2>
			<ul style="font-size:1.5em;font-weight: bold">
			<li>secret</li>
			<li>simple</li>
			<li>secure</li>
			</ul>
			<!--h2>... and delegate your voice if you cannot or don't want to vote by yourself.</h2-->
			<!--h3>
			Learn more about electric.vote:<br>
			<a href="https://www.youtube.de">- on our youtube channel</a><br>
			<a href="https://www.youtube.de">- in our tutorial</a><br>
			<a href="https://www.youtube.de">- from the press</a>
			</h3-->
			<h2>join now for free!</h2>
			</div>"""
		,"sign up conditions":
			"""<label for="accept">I read and accept the <a href="/legal/terms_of_use" style="text-decoration:underline">terms of use</a> and <a href="/legal/terms_of_use" style="text-decoration:underline">cookie policy</a></label>"""
		,"welcome reset password":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 40px">Forgot Password?</h1>
			<h2>... no problem ;)</h2>
			<h3>We'll send you an e-mail so you can reset your login credentials.</h3>
			</div>"""
		},
	"de":{
		"language_ID":"de"
		,"Login": "Anmelden"
		,"Logout": "Abmelden"
		,"Sign Up": "Registrieren"
		,"Password":"Passwort"
		,"Repeat Password":"Passwort wiederholen"
		,"Username":"Nutzername"
		,"Direct Vote":"direkte Stimme"
		,"Delegated Vote":"delegierte Stimme"
		,"click below to vote directly":"klicke unten, um direkt abzustimmen"
		,"Name":"Name"
		,"E-mail":"E-Mail"
		,"Send Circular":"Rundmail senden"
		,"Circular":"Rundmail"
		,"Donation":"Spende"
		,"Tutorial":"Tutorial"
		,"Feedback":"Rückmeldung"
		,"Imprint / Disclaimer":"Impressum / Haftungsausschluss"
		,"Imprint":"Impressum"
		,"Terms of Use":"Nutzungsbedingungen"
		,"Home":"Startseite"
		,"Open":"Offen"
		,"Group":"Gruppe"
		,"Voting":"Abstimmung"
		,"Closed":"Geschlossen"
		,"Filter":"Filter"
		,"Create Poll":"neue Umfrage"
		,"Leave Group":"Gruppe verlassen"
		,"New Group":"neue Gruppe"
		,"New":"Neu"
		,"Language":"Sprache"
		,"Delete":"Löschen"
		,"copy to clipboard":"Link kopieren"
		,"no invitation link":"kein Einladungslink"
		,"Grant Admin Rights in":"Administrator hinzufügen zu"
		,"Admin Options":"Administrator Optionen"
		,"Group Settings":"Gruppeneinstellungen"
		,"User Settings":"Benutzereinstellungen"
		,"Search":"Suche"
		,"Done":"Fertig"
		,"Remove Member from":"Mitglied entfernen von"
		,"Reset":"Zurücksetzen"
		,"Reset Password":"Passwort zurücksetzen"
		,"Remove":"Entfernen"
		,"Add Member to":"Mitglied hinzufügen zu"
		,"Settings":"Einstellungen"
		,"Add Member":"Mitglied hinzufügen"
		,"Invitation Link":"Einladungslink"
		,"Make Admin":"Administrator hinzufügen"
		,"Resign":"zurücktreten"
		,"Remove Member":"Mitglied entfernen"
		,"Delete Group":"Gruppe löschen"
		,"Profile Settings":"Profileinstellungen"
		,"Delete Account":"Account löschen"
		,"Polls":"Umfragen"
		,"Poll":"Umfrage"
		,"Result":"Ergebnis"
		,"Members can create choices":"Mitglieder können Möglichkeiten erstellen"
		,"Members can create polls":"Mitglieder können Umfragen erstellen"
		,"Comments":"Kommentare"
		,"Create Choice":"neue Möglichkeit"
		,"Author Options":"Autor Optionen"
		,"Evaluate":"Evaluiere"
		,"Poll Settings":"Umfrageeinstellungen"
		,"Delete Poll":"Umfrage löschen"
		,"Freeze Choices":"Abstimmungsphase"
		,"Freeze Votes":"beende Umfrage"
		,"Evaluation":"Evaluation"
		,"Secret":"Geheim"
		,"Not Secret":"Nicht Geheim"
		,"Choices":"Möglichkeiten"
		,"Choice":"Möglichkeit"
		,"Title":"Titel"
		,"Picture":"Bild"
		,"Description":"Beschreibung"
		,"Delete Choice":"Möglichkeit löschen"
		,"Your Vote":"Deine Stimme"
		,"Vote Weight":"Stimmgewicht"
		,"Participation":"Teilnahme"
		,"Result":"Resultat"
		,"Delegate Vote":"Delegiere Stimme"
		,"Choice Settings":"Einstellungen"
		,"Vote":"Stimme"
		,"Direct Votes":"Direkte Stimmen"
		,"Indirect Votes":"Indirekte Stimmen"
		,"Tags":"Tags"
		,"Create Comment":"neuer Kommentar"
		,"Submit":"Senden"
		,"Save":"Speichern"
		,"Create":"Senden"
		,"Cancel":"Abbrechen"
		,"Comment":"Kommentar"
		,"Delete Comment":"Kommentar löschen"
		,"welcome login":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 37px">Willkommen bei electric.vote!</h1>
			<h2 style="font-size: 21px">Hier kannst du gemeinsam Entscheidungen treffen - geheim, effizient und sicher.</h2>
			<a href="/reset_password"><h3 style="font-style: italic">- Passwort vergessen?</h3></a>
			</div>"""
		,"welcome sign up":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 37px">Willkommen bei electric.vote!</h1>
			<h2>Hier funktionieren Abstimmungen:</h2>
			<ul style="font-size:1.5em;font-weight: bold">
			<li>geheim</li>
			<li>effizient</li>
			<li>sicher</li>
			</ul>
			<h2>Bring dich ein und entscheide mit!</h2>
			</div>"""
		,"sign up conditions":
			"""<label for="accept">Ich habe die <a href="/legal/terms_of_use" style="text-decoration:underline">Cookie Richtlinie</a> und <a href="/legal/terms_of_use" style="text-decoration:underline">Nutzungsbedingungen</a> gelesen und akzeptiert.</label>"""
		,"name must not be empty": "Bitte geben Sie Ihren Namen an"
		,"username must consist of at least 4 letters. Only a-z,A-Z,.,_ are allowed": "Der Benutzername muss aus mind. 4 Buchstaben bestehen. Erlaubt sind a-z,A-Z,.,_"
		,"please enter a valid email":"Bitte geben Sie eine gültige E-Mail Adresse an"
		,"please accept our conditions":"Bitte akzeptieren Sie unsere Bedingungen"
		,"password must consist of at least 8 letters, a lower and an upper case character and a digit":"Das Passwort muss aus mind. 8 Buchstaben, einen Klein- / Gross-buchstaben und einer Zahl bestehen"
		,"welcome reset password":
			"""<div style="padding: 20px;max-width: 300px;width: 300px">
			<h1 style="font-size: 40px">Passwort vergessen?</h1>
			<h2>... kein Problem ;)</h2>
			<h3>Wir werden dir eine E-Mail schicken, sodass du deine Anmeldedaten zurücksetzen kannst.</h3>
			</div>"""
		,"no polls":"keine Umfragen"
		}
	}
