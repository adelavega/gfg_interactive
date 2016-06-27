def get_or_create(session, model, **kwargs):
	""" Checks to see if instance of model is in db. 
	If not add and commit. If true, return all matches.
	Args:
		session: db session
		model: Model class
		**kwargs: columns to filter by

	Returns:
		(all matching or created instances, if instance is new)
	"""
	instance = session.query(model).filter_by(**kwargs).first()
	if instance:
		return instance, False
	else:
		instance = model(**kwargs)
		session.add(instance)
		session.commit()
		return instance, True


def clean_db_string(string):
	string.replace("\t", "").replace(
            "\n", "").replace("'", "")

	return string

def gfg_user_exists(db_uri, userid):
	db_user, db_password = db_uri.split('/')[2].split('@')[0].split(':')
	import MySQLdb
	db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_password, db='gfg-research')
	cur = db.cursor()
	cur.execute("select Id from FBApp_Users_Status where id = %d" % int(userid))
	db.close()

	return len(cur.fetchall()) > 0