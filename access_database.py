import random
import json
import pymysql
import sys
import numpy as np
import tornado
import tornado.escape
from PIL import Image
import io
import datetime
from random import randint
import Certificates.passwords as pw

#how to set up database:
#login as "debian-sys-maint" ($ mysql -u debian-sys-maint -h localhost -p)
#use password as specified in /etc/mysql/debian.cnf
#create new user admin with passsword admin (> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';)
#grant and flush privileges (> GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';) (> FLUSH PRIVILEGES;)
#create database (> CREATE DATABASE liDem;)
#load database (> USE liDem; ) (> source /database/liDem.sql;)

url = "localhost"
database = "liDem"
username = pw.database_username
password = pw.database_password
read_timeout = 10
write_timeout = 10

weight_offset = 0.001

db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)

def esc(text):
	return tornado.escape.xhtml_escape(text)

def esc_m(text):
	return tornado.escape.linkify(text).replace('\n','<br>') #multi line

def select_one(query,args=None):
	global db
	for i in range(5):
		try:
			cursor = db.cursor()
			cursor.execute(query,args)
			data = cursor.fetchone()
			cursor.close()
			db.commit()
			return data
		except pymysql.err.InterfaceError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)
		except:
			pass

def select_all(query,args=None):
	global db
	for i in range(5):
		try:
			cursor = db.cursor()
			cursor.execute(query,args)
			data = cursor.fetchall()
			cursor.close()
			db.commit()
			return data
		except pymysql.err.InterfaceError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)
		except:
			pass

def insert(query,args=None):
	global db
	for i in range(5):
		try:
			cursor = db.cursor()
			cursor.execute(query,args)
			lastrowid = cursor.lastrowid
			cursor.close()
			db.commit()
			return lastrowid
		except pymysql.err.InterfaceError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)
		except pymysql.err.OperationalError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)

def update(query,args=None):
	global db
	for i in range(5):
		try:
			cursor = db.cursor()
			cursor.execute(query,args)
			cursor.close()
			db.commit()
			return
		except pymysql.err.InterfaceError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)
		except pymysql.err.OperationalError:
			db = pymysql.connect(url,username,password,database,read_timeout=read_timeout,write_timeout=write_timeout)

def save_image(request,file_object,username,folder,default):
	if file_object in request.files.keys() and len(request.files[file_object]) > 0:
		image = request.files[file_object][0]['body']
		img = Image.open(io.BytesIO(image)).convert("RGB")
		icon = f"{folder}/{username}_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{randint(0,9999999)}"
		img.save(f"static/{icon}_full.jpg")
		width,height = img.size
		medium_max_width = 1000
		medium_max_height = 1000
		img_medium = None
		if width>height and width>medium_max_width:
			img_medium = img.resize((medium_max_width,int(height*medium_max_width/width)),Image.ANTIALIAS)
		if height>width and height>medium_max_height:
			img_medium = img.resize((int(width*medium_max_height/height),medium_max_height),Image.ANTIALIAS)
		img_medium = img if img_medium is None else img_medium
		img_medium.save(f"static/{icon}.jpg")
		if width>height:
			img_small = img.crop(((width-height)/2,0,(width-height)/2+height,height)).resize((300,300),Image.ANTIALIAS)
		else:
			img_small = img.crop((0,(height-width)/2,width,(height-width)/2+width)).resize((300,300),Image.ANTIALIAS)
		img_small.save(f"static/{icon}_small.jpg")
		return icon
	return default

def user_convert(data):
	if data is None:
		return None
	user = {'id':data[0],'username':esc(data[1]),'username_unesc':data[1],'name':esc(data[2]),'name_unesc':data[2],'password':data[3],'description':esc_m(data[4]),'description_unesc':data[4],'icon':data[5]+".jpg",'icon_small':data[5]+"_small.jpg",'email':esc(data[6]),'reset_key':data[7],'reset_timestamp':data[8],'timestamp':data[9]}
	return user

def member_convert(data):
	if data is None:
		return None
	member = user_convert(data)
	member.update({'weight':data[10],'isAdmin':data[11]})
	return member

def group_convert(data):
	if data is None:
		return None
	return {'id':data[0],'name':esc(data[1]),'name_unesc':data[1],'motto':esc(data[2]),'motto_unesc':data[2],'description':esc_m(data[3]),'description_unesc':data[3],'icon':data[4]+".jpg",'icon_small':data[4]+"_small.jpg",'pollCreatorLevel':data[5],'invitationKey':data[6],'authorId':data[7],'timestamp':data[8]}

def poll_convert(data):
	if data is None:
		return None
	return {'id':data[0],'groupId':data[1],'title':esc(data[2]),'title_unesc':data[2],'description':esc_m(data[3]),'description_unesc':data[3],'secret':data[4],'phase':data[5],'icon':data[6]+".jpg",'icon_small':data[6]+"_small.jpg",'choiceCreatorLevel':data[7],'authorId':data[8],'timestamp':data[9],'endPhase0':data[10],'endPhase1':data[11],'authorUsername':esc(data[12]),'authorName':esc(data[13]),'authorName_unesc':data[13]}

def comment_convert(data):
	if data is None:
		return None
	return {'id':data[0],'groupId':data[1],'content':esc_m(data[2]),'authorId':data[3],'timestamp':data[4],'authorUsername':esc(data[5]),'authorName':esc(data[6]),'authorName_unesc':data[6],'n_answers':data[7],'tags':[]}

def choice_convert(data):
	if data is None:
		return None
	return {'id':data[0],'pollId':data[1],'title':esc(data[2]),'title_unesc':data[2],'description':esc_m(data[3]),'description_unesc':data[3],'icon':data[4]+".jpg",'icon_small':data[4]+"_small.jpg",'authorId':data[5],'timestamp':data[6]}

def choice_vote_convert(data):
	if data is None:
		return None
	choice = choice_convert(data)
	choice.update({'vote':data[7],'authorUsername':esc(data[8]),'authorName':esc(data[9]),'authorName_unesc':data[9]})
	return choice

def vote_convert(data):
	if data is None:
		return None
	return {'id':data[0],'userId':data[1],'choiceId':data[2],'vote':data[3],'timestamp':data[4]}

def follow_convert(data):
	if data is None:
		return None
	return {'id':data[0],'followerId':data[1],'followedId':data[2],'groupId':data[3],'weight':data[4],'timestamp':data[5]}

def get_user(userId):
	data = select_one("SELECT * FROM User WHERE ID = %s",userId)
	return user_convert(data)

def get_user_by_username(username):
	data = select_one("SELECT * FROM User WHERE Username = %s",username)
	return user_convert(data)

def create_user(username,password,name,email,description="",icon="icons/user"):
	try:
		insert("INSERT INTO User(Username,Name,Password,Description,Email,Icon) VALUES (%s,%s,%s,%s,%s,%s)",(username,name,password,description,email,icon))
		data = select_one("SELECT * FROM User WHERE User.Username = %s AND User.Password = %s",(username,password))
	except:
		return None
	return user_convert(data)

def log_user(userID,content):
	insert("INSERT INTO Log(UserID,Content) VALUES (%s,%s)",(userID,content))

def update_user(userId,password=None,name=None,email=None,description=None,icon=None,reset_key=None):
	try:
		if password is not None:
			update("UPDATE User SET Password=%s WHERE ID=%s",(password,userId))
		if name is not None:
			update("UPDATE User SET Name=%s WHERE ID=%s",(name,userId))
		if email is not None:
			update("UPDATE User SET Email=%s WHERE ID=%s",(email,userId))
		if description is not None:
			update("UPDATE User SET Description=%s WHERE ID=%s",(description,userId))
		if icon is not None:
			update("UPDATE User SET Icon=%s WHERE ID=%s",(icon,userId))
		if reset_key is not None:
			update("UPDATE User SET ResetKey=%s, ResetTimestamp=CURRENT_TIMESTAMP WHERE ID=%s",(reset_key,userId))
		data = select_one("SELECT * FROM User WHERE ID = %s",userId)
	except:
		print(sys.exc_info())
		return None
	return user_convert(data)

def reset_user_reset_key(userId):
	update("UPDATE User SET ResetKey=NULL, ResetTimestamp=NULL WHERE ID=%s",userId)
	return

def delete_user(userId):
	for group in get_groups(userId):
		leave_group(userId,group['id'])
	update("DELETE FROM User WHERE ID = %s",userId)
	update("DELETE FROM Log WHERE UserID = %s",userId)

def create_group(userId,name,motto,description,pollCreatorLevel=1,icon="icons/group"):
	try:
		club_id = insert("INSERT INTO Club(Name,Motto,Description,Icon,pollCreatorLevel,AuthorID) VALUES (%s,%s,%s,%s,%s,%s)",(name,motto,description,icon,pollCreatorLevel,userId))
		insert("INSERT INTO Member(UserID,ClubID,Level,GranterID) VALUES (%s,%s,'2',%s)",(userId,club_id,userId))
		data = select_one("SELECT * FROM Club WHERE ID = %s",club_id)
	except:
		return None
	return group_convert(data)

def update_group(groupId,name=None,motto=None,description=None,icon=None,pollCreatorLevel=None,invitationKey=None):
	try:
		if name is not None:
			update("UPDATE Club SET Name=%s WHERE ID=%s",(name,groupId))
		if motto is not None:
			update("UPDATE Club SET Motto=%s WHERE ID=%s",(motto,groupId))
		if description is not None:
			update("UPDATE Club SET Description=%s WHERE ID=%s",(description,groupId))
		if icon is not None:
			update("UPDATE Club SET Icon=%s WHERE ID=%s",(icon,groupId))
		if pollCreatorLevel is not None:
			update("UPDATE Club SET PollCreatorLevel=%s WHERE ID=%s",(pollCreatorLevel,groupId))
		if invitationKey is not None:
			update("UPDATE Club SET InvitationKey=%s WHERE ID=%s",(invitationKey,groupId))
		data = select_one("SELECT * FROM Club WHERE ID = %s",groupId)
	except:
		print(sys.exc_info())
		return None
	return group_convert(data)

def reset_group_invitation_key(groupId):
	update("UPDATE Club SET InvitationKey=NULL WHERE ID=%s",groupId)
	return

def get_group(groupId):
	data = select_one("SELECT * FROM Club WHERE Club.ID = %s",groupId)
	return group_convert(data)

def get_group_by_poll(pollId):
	data = select_one("SELECT Club.* FROM Club,Tender WHERE Club.ID = Tender.ClubID AND Tender.ID = %s",pollId)
	return group_convert(data)

def get_group_by_choice(choiceId):
	data = select_one("SELECT Club.* FROM Club,Tender,Proposal WHERE Club.ID = Tender.ClubID AND Tender.ID = Proposal.TenderID AND Proposal.ID = %s",choiceId)
	return group_convert(data)

def get_groups(userId):
	groups = []
	data = select_all("SELECT Club.* FROM Club,Member WHERE Club.ID = Member.ClubID AND Member.UserID = %s ORDER BY Member.Timestamp DESC",userId)
	for group in data:
		groups.append(group_convert(group))
	return groups

def get_common_groups(user1Id,user2Id):
	groups = []
	data = select_all("SELECT DISTINCT Club.*,member2.Timestamp FROM Club,Member member1,Member member2 WHERE Club.ID = member1.ClubID AND member1.UserID = %s AND Club.ID = member2.ClubID AND member2.UserID = %s ORDER BY member2.Timestamp DESC",(user1Id,user2Id))
	for group in data:
		groups.append(group_convert(group))
	return groups
	
def leave_group(userId,groupId):
	group_remove_member(userId,groupId)
	data = select_one("SELECT EXISTS(SELECT * FROM Member WHERE ClubID = %s AND Level = '2')",groupId)
	if data[0] == False:
		data = select_one("SELECT EXISTS(SELECT * FROM Member WHERE ClubID = %s)",groupId)
		if data[0] == False:
			delete_group(groupId)
		else:
			update("UPDATE Member SET Level = '2' WHERE ClubID = %s",groupId)

def resign_group(userId,groupId):
	update("UPDATE Member SET Level = '1' WHERE ClubID = %s AND UserID = %s",(groupId,userId))
	data = select_one("SELECT EXISTS(SELECT * FROM Member WHERE ClubID = %s AND Level = '2')",groupId)
	if data[0] == False:
		update("UPDATE Member SET Level = '2' WHERE ClubID = %s AND UserID <> %s",(groupId,userId))

def delete_group(groupId):
	update("DELETE FROM Club WHERE ID = %s",groupId)

def is_group_member(userId,groupId):
	data = select_one("SELECT EXISTS(SELECT * FROM Member WHERE ClubID = %s AND UserID = %s)",(groupId,userId))
	return data[0]

def is_group_admin(userId,groupId):
	data = select_one("SELECT EXISTS(SELECT * FROM Member WHERE ClubID = %s AND UserID = %s AND Level = '2')",(groupId,userId))
	return data[0]

def group_add_member(userId,groupId,granterId):
	try:
		insert("INSERT INTO Member(UserId,ClubId,GranterId,Level) VALUES (%s,%s,%s,'1')",(userId,groupId,granterId))
	except:
		print(sys.exc_info())
		return False
	return True

def group_remove_member(userId,groupId):
	update("DELETE FROM Member WHERE UserID = %s and ClubID = %s",(userId,groupId))
	update("DELETE FROM Comment WHERE AuthorID = %s and ClubID = %s",(userId,groupId))
	return

def group_make_admin(userId,groupId,granterId):
	update("UPDATE Member SET Level='2', GranterID = %s WHERE UserID=%s AND ClubID=%s",(granterId,userId,groupId))
	return

def get_group_users(groupId):
	data = select_all("SELECT User.* FROM User, Member WHERE Member.UserId = User.ID AND Member.ClubId = %s",(groupId))
	users = []
	for u in data:
		user = user_convert(u)
		users.append(user)
	return users

def get_group_members(userId,groupId,search=None):
	if search is None or search == "":
		data = select_all("SELECT User.*,Follow.Weight,Member.Level>=2 FROM User LEFT JOIN (SELECT * FROM Follow WHERE Follow.FollowerID = %s AND Follow.ClubId = %s) AS Follow ON User.ID = Follow.FollowedID, Member WHERE Member.UserId = User.ID AND Member.ClubId = %s AND User.ID <> %s ORDER BY Follow.Weight DESC",(userId,groupId,groupId,userId))
	else:
		data = select_all("SELECT User.*,Follow.Weight,Member.Level>=2, User.Username = %s AS equalName FROM User LEFT JOIN (SELECT * FROM Follow WHERE Follow.FollowerID = %s AND Follow.ClubId = %s) AS Follow ON User.ID = Follow.FollowedID, Member WHERE Member.UserId = User.ID AND Member.ClubId = %s AND User.ID <> %s AND (LOCATE(%s,User.Username)>0 OR LOCATE(%s,User.Name)>0) ORDER BY equalName DESC, Follow.Weight DESC",(search,userId,groupId,groupId,userId,search,search))
	total_weight = select_one("SELECT SUM(Follow.Weight),COUNT(*) FROM Follow WHERE Follow.FollowerID = %s AND Follow.ClubId = %s",(userId,groupId))[0]
	n_group_members = select_one("SELECT COUNT(*) FROM Member WHERE Member.ClubId = %s",groupId)[0]-1
	n_group_members = 1 if n_group_members==0 else n_group_members
	if total_weight is None:
		total_weight = 0
	members = []
	for user in data:
		member = member_convert(user)
		members.append(member)
		if member['weight'] is None:
			member['weight'] = 0
		member['weight_fraction'] = (member['weight']+weight_offset/n_group_members)/(total_weight+weight_offset)
	return members

def get_n_group_admins(groupId):
	data = select_one("SELECT COUNT(*) FROM Member WHERE Member.ClubId = %s AND Member.Level>=2",groupId)
	return data[0]

def get_group_member_suggestions(userId,groupId,name="",limit=5):
	data = select_all("SELECT User.*, (SELECT COUNT(*) FROM Club,Member m1,Member m2 WHERE Club.ID = m1.ClubID AND Club.ID = m2.ClubID AND m1.UserID=User.ID AND m2.UserID = %s) AS count, User.Username = %s AS equalName FROM User WHERE User.ID <> %s AND NOT EXISTS (SELECT * FROM Member WHERE Member.ClubID = %s AND Member.UserID = User.ID) AND (LOCATE(%s,User.Username)>0 OR LOCATE(%s,User.Name)>0) ORDER BY equalName DESC, count DESC LIMIT %s",(userId,name,userId,groupId,name,name,limit))
	members = []
	for user in data:
		members.append(user_convert(user))
	return members

def create_poll(userId,groupId,title,description,secret=True,phase=0,choiceCreatorLevel=1,icon="icons/poll"):
	try:
		secret = 1 if secret else 0
		pollId = insert("INSERT INTO Tender(ClubID,Title,Description,Secret,Phase,Icon,choiceCreatorLevel,AuthorID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(groupId,title,description,secret,phase,icon,choiceCreatorLevel,userId))
	except:
		print(sys.exc_info())
		return None
	return get_poll(pollId)

def get_poll(pollId):
	data = select_one("SELECT Tender.*,User.Username,User.Name FROM Tender,User WHERE Tender.ID = %s AND Tender.AuthorID=User.ID",pollId)
	return poll_convert(data)

def get_polls(groupId,phase=None):
	polls = []
	data = []
	if phase is None:
		data = select_all("SELECT Tender.*,User.Username,User.Name FROM Tender,User WHERE ClubId = %s AND Tender.AuthorID=User.ID ORDER BY Timestamp DESC",groupId)
	elif isinstance(phase,list):
		if len(phase)==0:
			return []
		query = "SELECT * FROM ( "
		params = ()
		for i,p in enumerate(phase):
			if i>0:
				query += " UNION "
			if p==0:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.Timestamp AS Time FROM Tender,User WHERE Tender.ClubID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			elif p==1:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.EndPhase0 AS Time FROM Tender,User WHERE Tender.ClubID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			elif p==2:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.EndPhase1 AS Time FROM Tender,User WHERE Tender.ClubID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			params = params + (groupId,p)
		query += ") AS T_ALL ORDER BY T_ALL.Time DESC"
		data = select_all(query,params)
	for poll in data:
		polls.append(poll_convert(poll))
	return polls

def get_polls_of_user(userId,phase=None):
	polls = []
	data = []
	if phase is None:
		data = select_all("SELECT Tender.*,User.Username,User.Name FROM Tender,Member,User WHERE Tender.ClubID = Member.ClubID AND Member.UserID = %s AND Tender.AuthorID=User.ID ORDER BY Tender.timestamp DESC",userId)
	elif isinstance(phase,list):
		if len(phase)==0:
			return []
		query = "SELECT * FROM ( "
		params = ()
		for i,p in enumerate(phase):
			if i>0:
				query += " UNION "
			if p==0:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.Timestamp AS Time FROM Tender,Member,User WHERE Tender.ClubID = Member.ClubID AND Member.UserID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			elif p==1:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.EndPhase0 AS Time FROM Tender,Member,User WHERE Tender.ClubID = Member.ClubID AND Member.UserID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			elif p==2:
				query += "SELECT Tender.*,User.Username,User.Name,Tender.EndPhase1 AS Time FROM Tender,Member,User WHERE Tender.ClubID = Member.ClubID AND Member.UserID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s"
			params = params + (userId,p)
		query += ") AS T_ALL ORDER BY T_ALL.Time DESC"
		data = select_all(query,params)
	else:
		data = select_all("SELECT Tender.*,User.Username,User.Name FROM Tender,Member,User WHERE Tender.ClubID = Member.ClubID AND Member.UserID = %s AND Tender.AuthorID=User.ID AND Tender.Phase = %s ORDER BY Tender.timestamp DESC",(userId,phase))
	for poll in data:
		polls.append(poll_convert(poll))
	return polls

def update_poll(pollId,title=None,description=None,icon=None,phase=None,choiceCreatorLevel=None):
	try:
		if title is not None:
			update("UPDATE Tender SET Title=%s WHERE ID=%s",(title,pollId))
		if description is not None:
			update("UPDATE Tender SET Description=%s WHERE ID=%s",(description,pollId))
		if icon is not None:
			update("UPDATE Tender SET Icon=%s WHERE ID=%s",(icon,pollId))
		if phase is not None:
			if phase==1:
				update("UPDATE Tender SET EndPhase0=CURRENT_TIMESTAMP WHERE ID=%s",(pollId))
			if phase==2:
				update("UPDATE Tender SET EndPhase1=CURRENT_TIMESTAMP WHERE ID=%s",(pollId))
			update("UPDATE Tender SET Phase=%s WHERE ID=%s",(phase,pollId))
		if choiceCreatorLevel is not None:
			update("UPDATE Tender SET ChoiceCreatorLevel=%s WHERE ID=%s",(choiceCreatorLevel,pollId))
	except:
		print(sys.exc_info())
		return None
	return get_poll(pollId)

def delete_poll(pollId):
	update("DELETE FROM Tender WHERE ID = %s",pollId)

def get_poll_by_choice(choiceId):
	data = select_one("SELECT Tender.*,User.Username,User.Name FROM Tender,Proposal,User WHERE Tender.ID = Proposal.TenderID AND Proposal.ID = %s AND Tender.AuthorID=User.ID",choiceId)
	return poll_convert(data)

def create_choice(userId,pollId,title,description,icon="icons/vote_2"):
	try:
		choiceId = insert("INSERT INTO Proposal(TenderID,Title,Description,Icon,AuthorID) VALUES (%s,%s,%s,%s,%s)",(pollId,title,description,icon,userId))
	except:
		print(sys.exc_info())
		return None
	return get_choice(userId,choiceId)

def get_choice(userId,choiceId):
	data = select_one("SELECT Proposal.*,Vote.Value,User.Username,User.Name FROM Proposal LEFT JOIN (SELECT * FROM Vote WHERE Vote.UserID=%s) AS Vote ON Proposal.ID=Vote.ProposalID,User WHERE Proposal.ID = %s AND Proposal.AuthorID = User.ID",(userId,choiceId))
	return choice_vote_convert(data)

def get_choices(userId,pollId):
	choices = []
	data = select_all("SELECT * FROM (SELECT Proposal.*,Vote.Value,User.Username,User.Name FROM Proposal LEFT JOIN (SELECT * FROM Vote WHERE Vote.UserID=%s) AS Vote ON Proposal.ID=Vote.ProposalID, User WHERE Proposal.TenderID = %s AND Proposal.AuthorID = User.ID ORDER BY Proposal.Timestamp DESC) AS RESULT ORDER BY RESULT.Value DESC",(userId,pollId))
	for choice in data:
		choices.append(choice_vote_convert(choice))
	return choices

def update_choice(userId,choiceId,title=None,description=None,icon=None):
	try:
		if title is not None:
			update("UPDATE Proposal SET Title=%s WHERE ID=%s",(title,choiceId))
		if description is not None:
			update("UPDATE Proposal SET Description=%s WHERE ID=%s",(description,choiceId))
		if icon is not None:
			update("UPDATE Proposal SET Icon=%s WHERE ID=%s",(icon,choiceId))
	except:
		print(sys.exc_info())
		return None
	return get_choice(userId,choiceId)

def get_vote(userId,choiceId):
	data = select_one("SELECT * FROM Vote WHERE UserID = %s AND ProposalID = %s",(userId,choiceId))
	return vote_convert(data)

def set_vote(userId,choiceId,vote):
	try:
		_vote = get_vote(userId,choiceId)
		if _vote is None:
			insert("INSERT INTO Vote(UserID,ProposalID,Value) VALUES (%s,%s,%s)",(userId,choiceId,vote))
		else:
			update("UPDATE Vote SET Value=%s, Timestamp=CURRENT_TIMESTAMP WHERE ID=%s",(vote,_vote['id']))
	except:
		print(sys.exc_info())
		return False
	return True

def delete_vote(userId,choiceId):
	update("DELETE FROM Vote WHERE Vote.UserID = %s AND Vote.ProposalID = %s",(userId,choiceId))

def delete_choice(choiceId):
	update("DELETE FROM Proposal WHERE ID = %s",choiceId)

def get_follow(followerId,followedId,groupId):
	data = select_one("SELECT * FROM Follow WHERE FollowerID = %s AND FollowedID = %s AND ClubID = %s",(followerId,followedId,groupId))
	return follow_convert(data)

def set_follow(followerId,followedId,groupId,weight):
	try:
		_follow = get_follow(followerId,followedId,groupId)
		if _follow is None:
			if weight != 0:
				insert("INSERT INTO Follow(FollowerID,FollowedID,ClubID,Weight) VALUES (%s,%s,%s,%s)",(followerId,followedId,groupId,weight))
		else:
			if weight >= 0 and weight <= 1:
				update("UPDATE Follow SET Weight=%s, Timestamp=CURRENT_TIMESTAMP WHERE ID=%s",(weight,_follow['id']))
	except:
		print(sys.exc_info())
		return False
	return True

def create_comment(userId,content,groupId):
	try:
		commentId = insert("INSERT INTO Comment(ClubID,Content,AuthorID) VALUES (%s,%s,%s)",(groupId,content,userId))
	except:
		print(sys.exc_info())
		return None
	return get_comment(commentId)

def get_comment(commentId):
	data = select_one("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User WHERE Comment.ID=%s AND Comment.AuthorID=User.ID",(commentId))
	return comment_convert(data)

def tag_comment_comment(commentId,commentedId):
	insert("INSERT INTO CommentComment(CommentID,CommentedID) VALUES (%s,%s)",(commentId,commentedId))

def tag_comment_poll(commentId,pollId):
	insert("INSERT INTO CommentTender(CommentID,TenderID) VALUES (%s,%s)",(commentId,pollId))

def tag_comment_choice(commentId,choiceId):
	insert("INSERT INTO CommentProposal(CommentID,ProposalID) VALUES (%s,%s)",(commentId,choiceId))

def get_comments_of_group(groupId):
	comments = []
	data = select_all("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User WHERE Comment.AuthorID=User.ID AND Comment.ClubID = %s AND NOT EXISTS(SELECT * FROM CommentComment cc WHERE cc.CommentID=Comment.ID) ORDER BY Comment.Timestamp DESC",(groupId)) # if you want to also include choice comments:  AND NOT EXISTS (SELECT * FROM CommentProposal cp WHERE cp.CommentID=Comment.ID)
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comments_of_poll(pollId):
	comments = []
	data = select_all("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User,CommentTender WHERE Comment.AuthorID=User.ID AND Comment.ID=CommentTender.CommentID AND CommentTender.TenderID = %s ORDER BY Comment.Timestamp DESC",(pollId))
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comments_of_choice(choiceId):
	comments = []
	data = select_all("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User,CommentProposal WHERE Comment.AuthorID=User.ID AND Comment.ID=CommentProposal.CommentID AND CommentProposal.ProposalID = %s ORDER BY Comment.Timestamp DESC",(choiceId))
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comments_of_comment(commentedId):
	comments = []
	data = select_all("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User,CommentComment WHERE Comment.AuthorID=User.ID AND Comment.ID=CommentComment.CommentID AND CommentComment.CommentedID = %s ORDER BY Comment.Timestamp DESC",(commentedId))
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comments_of_author(authorId):
	comments = []
	data = select_all("SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User WHERE Comment.AuthorID = User.ID AND User.ID = %s ORDER BY Comment.Timestamp DESC",(authorId))
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comments_of_author_related_to_user(authorId,userId):
	comments = []
	data = select_all("""SELECT Comment.*,User.Username,User.Name,(SELECT COUNT(*) FROM CommentComment cc WHERE cc.CommentedID=Comment.ID) AS n_answers FROM Comment,User WHERE Comment.AuthorID = %s AND User.ID = %s AND (EXISTS(SELECT * FROM Member m WHERE m.UserID = %s AND m.ClubID = Comment.ClubID)) ORDER BY Comment.Timestamp DESC""",(authorId,authorId,userId))
	for comment in data:
		comments.append(comment_convert(comment))
	return comments

def get_comment_tags(commentId,exclude=[]):
	tags = []
	if "comment" not in exclude:
		data = select_all("SELECT CommentedID FROM CommentComment WHERE CommentID = %s",(commentId))
		for tag in data:
			tags.append({"link":"comment","id":tag[0],"tag":"comment","tag_unesc":"comment"})
	if "group" not in exclude:
		data = select_all("SELECT Club.ID,Club.Name FROM Club,Comment WHERE Comment.ID = %s AND Comment.ClubID = Club.ID",(commentId))
		for tag in data:
			tags.append({"link":"group","id":tag[0],"tag":esc(tag[1]),"tag_unesc":tag[1]})
	if "poll" not in exclude:
		data = select_all("SELECT TenderID,Title FROM CommentTender,Tender WHERE CommentID = %s AND TenderID = ID",(commentId))
		for tag in data:
			tags.append({"link":"poll","id":tag[0],"tag":esc(tag[1]),"tag_unesc":tag[1]})
	if "choice" not in exclude:
		data = select_all("SELECT ProposalID,Title FROM CommentProposal,Proposal WHERE CommentID = %s AND ProposalID = ID",(commentId))
		for tag in data:
			tags.append({"link":"choice","id":tag[0],"tag":esc(tag[1]),"tag_unesc":tag[1]})
	if "user" not in exclude:
		data = select_all("SELECT Username,Name FROM CommentUser,User WHERE CommentID = %s AND UserID=ID",(commentId))
		for tag in data:
			tags.append({"link":"user","id":tag[0],"tag":esc(tag[1]),"tag_unesc":tag[1]})
	return tags

def add_tags_to_comments(comments,exclude=[]):
	for comment in comments:
		comment["tags"] = get_comment_tags(comment['id'],exclude)
	return comments

def delete_comment(commentId):
	update("DELETE FROM Comment WHERE ID = %s",commentId)

def evaluate_poll(userId,pollId):

	# here comes the core of LiDem...
	poll = get_poll(pollId)
	
	# make new evaluation entry
	evaluation_id = insert("INSERT INTO Evaluation(TenderID,AuthorID) VALUES (%s,%s)",(pollId,userId))
	
	# get list of follower weights
	data = select_all("SELECT FollowerID,FollowedID,Weight FROM Follow WHERE ClubID = %s AND Weight <> 0",(poll['groupId']))
	followers = []
	for follower in data:
		followers.append([follower[0],follower[1],follower[2]])
	
	# make a loop over all choices
	data = select_all("SELECT * FROM Proposal WHERE TenderID = %s",(pollId))
	for choice in data:
		# get users and weather they have voted
		data = select_all("SELECT User.ID,(EXISTS (SELECT * FROM Vote WHERE Vote.ProposalID = %s AND Vote.UserID = User.ID)) FROM User,Member WHERE Member.UserID = User.ID AND Member.ClubID = %s",(choice[0],poll['groupId']))
		users_voted = []
		users_not_voted = []
		for user in data:
			if user[1]==0:
				users_not_voted.append(user[0])
			else:
				users_voted.append(user[0])
		
		# build up follow matrix
		n_not_voted = len(users_not_voted)
		n_voted = len(users_voted)
		not_voted_not_voted = np.ones([n_not_voted,n_not_voted])/(n_not_voted+n_voted)*weight_offset
		not_voted_voted = np.ones([n_not_voted,n_voted])/(n_not_voted+n_voted)*weight_offset
		for follower in followers:
			if follower[0] in users_not_voted:
				if follower[1] in users_not_voted:
					not_voted_not_voted[users_not_voted.index(follower[0]),users_not_voted.index(follower[1])] += follower[2]
				else:
					not_voted_voted[users_not_voted.index(follower[0]),users_voted.index(follower[1])] += follower[2]
		
		normalizer = np.expand_dims(np.sum(not_voted_not_voted,axis=1)+np.sum(not_voted_voted,axis=1),axis=1)
		not_voted_not_voted = np.divide(not_voted_not_voted, normalizer)
		not_voted_voted = np.divide(not_voted_voted, normalizer)
		try:
			# build up vote vector
			votes = np.zeros([n_voted,1])
			data = select_all("SELECT UserID,Value FROM Vote WHERE ProposalID = %s",(choice[0]))
			for i,vote in enumerate(data):
				votes[users_voted.index(vote[0]),0]=vote[1]
			
			follow_matrix = np.matmul(np.linalg.inv(np.eye(n_not_voted)-not_voted_not_voted),not_voted_voted)
			
			indirect_votes = np.matmul(follow_matrix,votes)
			result = (np.sum(votes)+np.sum(indirect_votes))/(n_voted+n_not_voted)
			weights = np.sum(follow_matrix,axis=0)+1
			
		except np.linalg.LinAlgError as e:
			print(e)
			result = 0
			indirect_votes = np.zeros([n_not_voted,1])
		
		# make new result entry
		resultId = insert("INSERT INTO Result(EvaluationID,ProposalID,Outcome) VALUES (%s,%s,%s)",(evaluation_id,choice[0],float(result)))
		
		# make result details
		for i in range(len(votes)):
			insert("INSERT INTO ResultDetail(ResultID,UserID,Weight,Value) VALUES (%s,%s,%s,%s)",(str(resultId),str(users_voted[i]),str(weights[i]),str(votes[i][0])))
		for i in range(len(indirect_votes)):
			insert("INSERT INTO ResultDetail(ResultID,UserID,Weight,Value) VALUES (%s,%s,%s,%s)",(str(resultId),str(users_not_voted[i]),"0",str(indirect_votes[i][0])))
	
	return

def get_all_evaluations(pollId):
	evaluation = get_latest_evaluation(pollId)
	if evaluation is None:
		return evaluation
	for result in evaluation["results"]:
		data = select_all("SELECT Evaluation.Timestamp, Result.Outcome FROM Result,Evaluation WHERE Result.EvaluationID = Evaluation.ID AND Result.ProposalID = %s",(result["proposal"]["id"]))
		all_results = []
		for data_point in data:
			all_results.append({"timestamp":data_point[0],"result":data_point[1]})
		result["all_results"] = all_results
	return evaluation

def get_latest_evaluation(pollId):
	data = select_one("SELECT Evaluation.Timestamp,Evaluation.ID FROM Evaluation WHERE TenderID = %s ORDER BY Evaluation.Timestamp DESC",(pollId))
	if data is None:
		return None
	timestamp = data[0]
	results = []
	
	data = select_all("SELECT Proposal.*,Result.Outcome FROM Result,Proposal WHERE Result.EvaluationID = %s AND Result.ProposalID = Proposal.ID ORDER BY Result.Outcome DESC",(data[1]))
	for choice in data:
		results.append({"proposal":choice_convert(choice),"result":choice[-1]})
	return {"results":results, "timestamp":timestamp}

def get_evaluation_details(choiceId):
	data = select_one("SELECT Result.ID,Result.Outcome,Evaluation.Timestamp FROM Result, Evaluation WHERE Result.ProposalID = %s AND Result.EvaluationID = Evaluation.ID ORDER BY Evaluation.Timestamp DESC",(choiceId))
	
	if data is None:
		return None
	resultId = data[0]
	result = data[1]
	timestamp = data[2]
	results = []
	n_direct_votes = 0
	n_indirect_votes = 0
	
	data = select_all("SELECT User.*,ResultDetail.Weight,ResultDetail.Value FROM ResultDetail,User WHERE ResultDetail.ResultID=%s AND ResultDetail.UserID=User.ID ORDER BY ResultDetail.Weight DESC",(resultId))
	for vote in data:
		if vote[-2] != 0:
			n_direct_votes += 1
		else:
			n_indirect_votes += 1
		results.append({"user":user_convert(vote),"weight":vote[-2],"value":vote[-1]})
	return {"n_direct_votes":n_direct_votes,"n_indirect_votes":n_indirect_votes,"results":results,"result":result,"timestamp":timestamp}
