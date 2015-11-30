from database import db
# from sqlalchemy.dialects.postgresql import JSON
import datetime
import io, csv, json


class Participant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    gfgid = db.Column(db.String())      
     
    browser = db.Column(db.String())
    platform = db.Column(db.String())
    language = db.Column(db.String())		#????

    experimentname = db.Column(db.String())
    arrive = db.Column(db.DateTime)
    beginexp = db.Column(db.DateTime)
    endexp = db.Column(db.DateTime)
    status = db.Column(db.Integer(), default = 1)
    debug = db.Column(db.Boolean)
    datastring = db.Column(db.Text)

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.status = 1
        self.arrive = datetime.datetime.now()


    def get_trial_data(self):
        """ Refactor this to use postegresql json functions and reflect actualall_correct_responses.to_csv('all_correct_responses.csv',index=False,header=False) experiments. 
        Maybe leave with some flexibility though..."""
        try:
            trialdata = json.loads(self.datastring)["data"]
        except:
            # There was no data to return.
            print("No trial data found in record:", self)
            return("")

        try:
            ret = []
            with io.BytesIO() as outstring:
                csvwriter = csv.writer(outstring)
                for trial in trialdata:
                    csvwriter.writerow((
                        self.gfgid,
                        trial["current_trial"],
                        trial["dateTime"],
                        json.dumps(trial["trialdata"])))
                ret = outstring.getvalue()
            return ret
        except:
            print("Error reading record:", self)
            return("")

    def get_event_data(self):
        try:
            eventdata = json.loads(self.datastring)["eventdata"]
        except (ValueError, TypeError):
            # There was no data to return.
            print("No event data found in record:", self)
            return("")
        
        try:
            ret = []
            with io.BytesIO() as outstring:
                csvwriter = csv.writer(outstring)
                for event in eventdata:
                    csvwriter.writerow((self.gfgid, event["eventtype"], event["interval"], event["value"], event["timestamp"]))
                ret = outstring.getvalue()
            return ret
        except:
            print("Error reading record:", self)
            return("")

    def __repr__(self):
        return "Subject(%s, %s, %s)" % ( 
            self.gfgid, 
            self.status,
            self.experimentname)

########################################### STORE USER ##################################
#Store_user Table - central table for user ids (same as Particpant(old))
class Store_user(db.Model):
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
    block = db.Column(db.String(100))
    question = db.Column(db.String(20))
    answer = db.Column(db.String(20))
    user_answer = db.Column(db.String(20))
    beginexp = db.Column(db.DateTime)

    # Return each row just like that
    def __repr__(self):
        return "CS Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" %(self.cs_id, self.gfgid, self.sess_id, self.response, self.reaction_time, 
        	self.accuracy, self.block, self.question, self.answer, self.user_answer, self.beginexp, self.trial_num)


