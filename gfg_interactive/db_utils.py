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

def gfg_user_exists(userid, db_host, db_user, db_password, db_name):
	""" Check the gfg core research database for matching userid """
	import MySQLdb
	db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_password, db=db_name)
	cur = db.cursor()
	cur.execute("select user_id from FBApp_Users_Status where user_id = %d" % int(userid))
	db.close()

	## Did this query return anything? I.e. are there any users in the main db with this id?
	return len(cur.fetchall()) > 0

def get_age_matched_ids(userid, db_host, db_user, db_password, db_name):
	""" Gets the gfg_ids of users that make another users age """
	import MySQLdb
	db = MySQLdb.connect(host="localhost", user=db_user, passwd=db_password, db=db_name)
	cur = db.cursor()
	cur.execute("select age_range from FBApp_Users_Ids where id = %d" % int(userid))

	age_range = cur.fetchone()

	cur.execute("select id from FBApp_Users_Ids where age_range = %d" % int(age_range[0]))
	db.close()

	return cur.fetchall()
