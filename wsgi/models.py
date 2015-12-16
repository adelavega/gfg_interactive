from database import db

########################################### STORE USER ##################################
#Store_user Table - central table for user ids (same as Particpant(old))
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False)
    
    # Return each row just like that
    def __repr__(self):
        return "Store_user values (%s, %s)" %(self.id, self.gfgid)


###########################################  SESSION ##################################
#Session Table - all about the session
class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False)  #coz each user can have multiple sessions
    browser = db.Column(db.String(), nullable=False)
    platform = db.Column(db.String(), nullable=False)
    debug = db.Column(db.Boolean)   #not sure if this is needed or not
    status = db.Column(db.Integer(), nullable=False)   #needs discussion after refactoring
    exp_name = db.Column(db.String(), nullable=False)
    begin_session = db.Column(db.DateTime, nullable=False)

    # Return each row just like that
    def __repr__(self):
        return "Session values (%s, %s, %s, %s, %s, %s, %s, %s)" %(self.session_id, self.gfgid, self.browser, self.platform, self.exp_name, self.status, self.debug, self.begin_session)


###########################################  CATEGORY SWITCH ##################################
#Experiment - Category Switch
class CategorySwitch(db.Model):
    cs_id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False)  
    sess_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))    # FORIEGN KEY
    trial_num = db.Column(db.Integer)
    response = db.Column(db.String(2))  # J or K key pressed
    reaction_time = db.Column(db.Float) # Reaction time in seconds- depends on what level of accuracy we want
    accuracy = db.Column(db.Integer) # calculated based on a number of factors
    block = db.Column(db.Unicode)
    question = db.Column(db.Unicode)	# TBD
    answer = db.Column(db.Unicode)		# TBD
    user_answer = db.Column(db.Unicode)	# TBD
    beginexp = db.Column(db.DateTime)

    # Return each row just like that
    """def __repr__(self):
        return "CS Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %(self.cs_id, self.gfgid, self.sess_id, self.response, self.reaction_time, 
        	self.accuracy, self.block, self.question, self.answer, self.user_answer, self.beginexp, self.trial_num)"""

###########################################  CATEGORY SWITCH ##################################
#Experiment - Category Switch
class KeepTrack(db.Model):
    kt_id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False)  
    sess_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))    # FORIEGN KEY
    trial_num = db.Column(db.Integer)
    reaction_time = db.Column(db.Float) # Reaction time in seconds- depends on what level of accuracy we want
    accuracy = db.Column(db.String) # calculated based on a number of factors
    block = db.Column(db.Unicode)
    beginexp = db.Column(db.DateTime)
    target_word1 = db.Column(db.String)
    target_word2 = db.Column(db.String)
    target_word3 = db.Column(db.String)
    target_word4 = db.Column(db.String)
    target_word5 = db.Column(db.String)
    input_word1 = db.Column(db.String)
    input_word2 = db.Column(db.String)
    input_word3 = db.Column(db.String)
    input_word4 = db.Column(db.String)
    input_word5 = db.Column(db.String)
    
    # Return each row just like that
    """def __repr__(self):
        return "KT Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %(self.cs_id, self.gfgid, self.sess_id, self.response, self.reaction_time, 
        	self.accuracy, self.block, self.question, self.answer, self.user_answer, self.beginexp, self.trial_num)"""


###########################################  EVENT DATA ##################################
# For all Experiments
class EventData(db.Model):
	ev_id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
	gfgid = db.Column(db.String(), nullable=False)
	sess_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))    # FORIEGN KEY
	exp_name = db.Column(db.String(), nullable=False)
	event_type = db.Column(db.String(), nullable=False)
	value_1 = db.Column(db.String())
	value_2 = db.Column(db.String())
	value_3 = db.Column(db.String())
	interval = db.Column(db.Float)
	timestamp = db.Column(db.DateTime)	#to store the timestamp.