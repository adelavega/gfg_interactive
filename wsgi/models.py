from database import db
import datetime
from flask import current_app
from db_utils import clean_db_string


class User(db.Model):
    """ User id table """
    id = db.Column(db.Integer, primary_key=True)
    gfg_id = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "Store_user values (%s, %s)" % (self.id, self.gfg_id)


class Session(db.Model):
    """ Session table. One is allocated per new valid visit """
    session_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(), nullable=False)
    browser = db.Column(db.String(), nullable=False)
    platform = db.Column(db.String(), nullable=False)
    status = db.Column(db.Integer(), nullable=False)
    exp_name = db.Column(db.String(), nullable=False)
    begin_session = db.Column(db.DateTime, nullable=False)
    begin_experiment = db.Column(db.DateTime)
    datastring = db.Column(db.String())

    def __repr__(self):
        return "Session values (%s, %s, %s, %s, %s, %s, %s, %s)" % (self.session_id,
            self.gfg_id, self.browser, self.platform, self.exp_name, self.status,
            self.debug, self.begin_session)


class CategorySwitch(db.Model):
    """ CategorySwitch experiment table """
    cs_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(), nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.session_id'))
    trial_num = db.Column(db.Integer)
    response = db.Column(db.String(2))
    reaction_time = db.Column(db.Float) 
    accuracy = db.Column(db.Integer)
    block = db.Column(db.Unicode)
    question = db.Column(db.Unicode)  # TBD
    answer = db.Column(db.Unicode)      # TBD
    user_answer = db.Column(db.Unicode)  # TBD
    timestamp = db.Column(db.DateTime)

    # Return each row just like that
    def __repr__(self):
        return "CS Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (self.cs_id, self.gfg_id,
            self.session_id, self.response, self.reaction_time, self.accuracy, self.block,
            self.question, self.answer, self.user_answer, self.beginexp, self.trial_num)

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
        self.timestamp = datetime.datetime.fromtimestamp(jsts/1000.0)

        # Remove invalid charachters from block name (e.g. "\n")
        self.block = clean_db_string(trial_data['block'])

        current_app.logger.info(
            "%s added to CategorySwitch for session id %s " % (self.trial_num, self.session_id))


class KeepTrack(db.Model):
    """ KeepTrack experiment table """
    kt_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(), nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.session_id')) 
    trial_num = db.Column(db.Integer)
    reaction_time = db.Column(db.Float)
    accuracy = db.Column(db.String)
    block = db.Column(db.Unicode)
    timestamp = db.Column(db.DateTime)
    target_words = db.Column(db.String)
    input_words = db.Column(db.String)

    ### FIX
    def __repr__(self):
        return "KT Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (self.cs_id, self.gfg_id, 
        self.session_id, self.response, self.reaction_time, self.accuracy, self.block, 
        self.question, self.answer, self.user_answer, self.beginexp, self.trial_num)

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

        self.target_words = trial_data['target_words']
        self.input_words = trial_data['input_words']

        # Datetime conversion
        self.timestamp= datetime.datetime.fromtimestamp(json_trial['dateTime']/1000.0)
        self.block = clean_db_string(trial_data['block'])


class EventData(db.Model):
    """ EventData for all experiments """
    ev_id = db.Column(db.Integer, primary_key=True) 
    gfg_id = db.Column(db.String(), nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.session_id'))
    exp_name = db.Column(db.String(), nullable=False)
    event_type = db.Column(db.String(), nullable=False)
    value_1 = db.Column(db.String())
    value_2 = db.Column(db.String())
    value_3 = db.Column(db.String())
    interval = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)  # to store the timestamp.

    def __repr__(self):
        pass

    def add_json_data(self, json_event):
        """ Parse and add backbone.js json data for a event """
        # self.event_type = 

        if isinstance(['value'], list):
            self.value_1 = str(json_event['value'][0])
            self.value_2 = str(json_event['value'][1])
            self.value_3 = str(json_event['value'])
        # self.interval = 
        self.timestamp = datetime.datetime.fromtimestamp(json_event['timestamp']/1000.0)
