from database import db
from flask import current_app
from db_utils import clean_db_string
from utils import convert_timestamp


class Participant(db.Model):
    """ Participant id table """
    id = db.Column(db.Integer, primary_key=True)
    gfg_id = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return "Store_user values (%s, %s)" % (self.id, self.gfg_id)


class Session(db.Model):
    """ Session table. One is allocated per new valid visit """
    session_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(32), nullable=False)
    browser = db.Column(db.String(32), nullable=False)
    platform = db.Column(db.String(32), nullable=False)
    status = db.Column(db.Integer(), nullable=False)
    exp_name = db.Column(db.String(32), nullable=False)
    begin_session = db.Column(db.DateTime, nullable=False)
    begin_experiment = db.Column(db.DateTime)
    datastring = db.Column(db.String(32))

    def __repr__(self):
        return "Session values (%s, %s, %s, %s, %s)" % (self.session_id,
            self.gfg_id,self.exp_name, self.status, self.begin_session)


class CategorySwitch(db.Model):
    """ CategorySwitch experiment table """
    cs_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(32), nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.session_id'))
    trial_num = db.Column(db.Integer)
    response = db.Column(db.String(2))
    reaction_time = db.Column(db.Float) 
    accuracy = db.Column(db.Integer)
    block = db.Column(db.Unicode(32))
    question = db.Column(db.Unicode(32))  # TBD
    answer = db.Column(db.Unicode(32))      # TBD
    user_answer = db.Column(db.Unicode(32))  # TBD
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return "CS Values (%s, %s, %s, %s)" % (self.cs_id, self.gfg_id,
            self.session_id, self.trial_num)

    def add_json_data(self, json_trial):
        """ Parse and add backbone.js json data for a trial """
        self.trial_num = json_trial['current_trial']

        # Parse nested JSON data to extract, acc, RT
        trial_data = json_trial['trialdata']

        self.response = trial_data['resp']

        # TODO: Add specific stimuli. Requires editing JSON
        self.question = "null"
        self.answer = "null"
        self.user_answer = "null"

        # Special case for accuracy
        if trial_data['acc'] == "FORWARD":
            self.accuracy = 11
        elif trial_data['acc'] == "BACK":
            self.accuracy = 22
        elif trial_data['acc'] == "NA":
            self.accuracy = 99
        else:
            self.accuracy = trial_data['acc']

        # Special case for reaction time
        if trial_data['rt'] == "NA":
            self.reaction_time = 00
        else:
            self.reaction_tiome = trial_data['rt']

        # Datetime conversion
        jsts = json_trial['dateTime']  # Javscript timestamp
        self.timestamp = convert_timestamp(jsts)

        # Remove invalid charachters from block name (e.g. "\n")
        self.block = clean_db_string(trial_data['block'])

        current_app.logger.info(
            "%s added to CategorySwitch for session id %s " % (self.trial_num, self.session_id))


class KeepTrack(db.Model):
    """ KeepTrack experiment table """
    kt_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(32), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id')) 
    trial_num = db.Column(db.Integer)
    reaction_time = db.Column(db.Float)
    accuracy = db.Column(db.String(32))
    block = db.Column(db.Unicode(32))
    timestamp = db.Column(db.DateTime)
    target_words = db.Column(db.Unicode(32))
    input_words = db.Column(db.Unicode(32))

    ### FIX
    def __repr__(self):
        return "KT Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (self.kt_id, self.gfg_id, 
        self.session_id, self.trial_num, self.reaction_time, self.accuracy, self.block, 
        self.timestamp, self.target_words, self.input_words)

    def add_json_data(self, json_trial):
        """ Parse and add backbone.js json data for a trial """

        self.trial_num = json_trial['current_trial']
        trial_data = json_trial['trialdata']

        if 'rt' not in trial_data:
            self.reaction_time = 00
        else:
            self.reaction_Time = trial_data['rt']

        if 'acc' not in trial_data:
            self.accuracy = "null"
        else:
            self.accuracy = trial_data['acc']

        if 'target_words' not in trial_data:
        	self.target_words = "null"
        else:
        	self.target_words = ",".join(trial_data['target_words']) # [u'Mile', u'Cat', u'France']-->u'Mile,Cat,France'

        if 'input_words' not in trial_data:
        	self.input_words = "null"
        else:
        	self.input_words = ",".join(trial_data['input_words'])

        # Datetime conversion
        self.timestamp= convert_timestamp(json_trial['dateTime'])
        self.block = clean_db_string(trial_data['block'])

        current_app.logger.info(
            "%s added to KeepTrack for session id %s " % (self.trial_num, self.session_id))


class EventData(db.Model):
    """ EventData for all experiments """
    ev_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(32), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'))
    exp_name = db.Column(db.String(32), nullable=False)
    event_type = db.Column(db.String(32))
    value = db.Column(db.Unicode(32)) ## Why split into three?
    interval = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False)  # to store the timestamp.

    def __repr__(self):
        pass

    def add_json_data(self, json_event):
        """ Parse and add backbone.js json data for a event """
 	
        self.event_type = json_event['eventtype']
        self.value = str(json_event['value'])

        # if isinstance(['value'], list):
        #     self.value_1 = str(json_event['value'][0])
        #     self.value_2 = str(json_event['value'][1])
        #     self.value_3 = str(json_event['value'])
        # self.interval = 
	self.interval = json_event['interval']
        self.timestamp = convert_timestamp(json_event['timestamp'])

        current_app.logger.info(
            "%s added to EventData for session id %s and whole eventJSON is %s " % (self.ev_id, self.session_id, json_event))

class QuestionData(db.Model):
    """ Feedback-form question-data for all experiments """
    q_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(32), nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.session_id'))
    exp_name = db.Column(db.String(32), nullable=False)
    rating = db.Column(db.String(32))          
    difficulty = db.Column(db.String(32)) 
    distraction = db.Column(db.String(32))      #informative
    #extrahelp = db.Column(db.String)        #added new
    openended = db.Column(db.Unicode(32))

    def __repr__(self):
        pass

    def add_json_data(self, json_event):
        """ Parse and add backbone.js json data for a questionnaire """
        self.rating = json_event['rating']
        if json_event['difficulty'] == "Not difficult":
            json_event['difficulty'] = "1"
        elif json_event['difficulty'] == "Somewhat difficult":
            json_event['difficulty'] = "5"
        elif json_event['difficulty'] == "Very difficult":
            json_event['difficulty'] = "10"
        elif json_event['difficulty'] == "Not rated":
            json_event['difficulty'] = "0"
        self.difficulty = json_event['difficulty']
      
        if json_event['distraction'] == "No distraction":
            json_event['distraction'] = "1"
        elif json_event['distraction'] == "Some distractions":
            json_event['distraction'] = "5"
        elif json_event['distraction'] == "Frequent interruptions":
            json_event['distraction'] = "10"
        elif json_event['distraction'] == "Not rated":
            json_event['distraction'] = "0"
        self.distraction = json_event['distraction']
       
        #self.extrahelp = json_event['extrahelp']
        self.openended = clean_db_string(json_event['openended'])	

        current_app.logger.info(
            "%s added to QuestionData for session id %s " % (self.q_id, self.session_id))
       
