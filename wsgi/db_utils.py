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