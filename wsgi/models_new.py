from database import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
import io, csv, json
import os, platform     #to get the platform information

###########################################  PARTICPANT ##################################
#Central Table with all the ids
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False, unique=True)      
     
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

    # Return each row just like that
    def __repr__(self):
        return "Data is (%s, %s)" % ( 
            self.id, 
            self.gfgid)

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

    # Return each row just like that
    def __repr__(self):
        return "Ids (%s, %s) ...... System Info(%s, %s) .... Exp Info(%s, %s, %s)" % 
        (self.id, self.gfgid, 
        self.browser, self.platform,
        self.exp_name, self.status, self.debug)

###########################################  CATEGORY SWITCH ##################################
#Experiment - Category Switch
class CategorySwitch(db.Model):
    cs_id = db.Column(db.Integer, primary_key=True)    # PRIMARY KEY 
    gfgid = db.Column(db.String(), nullable=False)  
    sess_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))    # FORIEGN KEY
    response = db.Column(db.String(2), nullable=False)  # J or K key pressed
    reaction_time = db.Column(db.Float, nullable=False) # Reaction time in seconds- depends on what level of accuracy we want
    accuracy = db.Column(db.Integer) # calculated based on a number of factors
    block = db.Column(db.String(20), nullable=False)
    question = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(20), nullable=False)
    user_answer = block = db.Column(db.String(20), nullable=False)
    beginexp = db.Column(db.DateTime, nullable=False)
    endexp = db.Column(db.DateTime, nullable=False)

###########################################  KEEP TRACK ##################################
#Experiment - Keep Track (TBD)