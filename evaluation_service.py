from access_database import *
import time
from tornado.options import define, options

def select_all_temporary(queries,args=None):
	global db
	for i in range(5):
		try:
			cursor = db.cursor()
			for i,query in enumerate(queries):
				if args is None:
					cursor.execute(query,None)
				else:
					cursor.execute(query,args[i])
			data = cursor.fetchall()
			cursor.close()
			db.commit()
			return data
		except pymysql.err.InterfaceError as e:
			print(e)
			db = pymysql.connect(url,username,password,database)
		except Exception as e:
			print(e)

def get_polls_to_update():
	data = select_all_temporary(["DROP TEMPORARY TABLE IF EXISTS last_eval","CREATE TEMPORARY TABLE last_eval SELECT Tender.*,User.Username,User.Name,(SELECT MAX(Timestamp) as last_evaluation FROM Evaluation WHERE Evaluation.TenderID = Tender.ID) as last_evaluation FROM Tender,User WHERE Tender.Phase < 2 AND Tender.AuthorID=User.ID","SELECT * FROM last_eval WHERE EXISTS (SELECT * FROM Proposal,Vote WHERE Proposal.ID = Vote.ProposalID AND Proposal.TenderID = last_eval.ID AND Vote.Timestamp > last_eval.last_evaluation) OR EXISTS (SELECT * FROM Proposal WHERE Proposal.TenderID = last_eval.ID AND Proposal.Timestamp > last_eval.last_evaluation) OR EXISTS (SELECT * FROM Follow WHERE Follow.ClubID = last_eval.ClubID AND Follow.Timestamp > last_eval.last_evaluation) OR last_eval.last_evaluation IS NULL"])
	polls = []
	for poll in data:
		tmp = poll_convert(poll)
		tmp["last_evaluation"] = poll[-1]
		polls.append(tmp)
	return polls

if __name__=="__main__":
	define("frequency", default=5, help="frequency of checking polls to evaluate [in minutes] (default: 5)", type=float)
	options.parse_command_line()
	while True:
		for poll in get_polls_to_update():
			print(f"evaluate: {poll['title_unesc']}")
			try:
				evaluate_poll(-1,poll['id'])
			except Exception as e:
				print(e)
		time.sleep(options.frequency*60)
