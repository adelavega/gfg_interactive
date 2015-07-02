from database import db
# from sqlalchemy.dialects.postgresql import JSON
import datetime
import io, csv, json


class Participant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uniqueid = db.Column(db.String(), primary_key=True)
    ipaddress = db.Column(db.String())

    ipaddress = db.Column(db.String())
    browser = db.Column(db.String())
    platform = db.Column(db.String())
    language = db.Column(db.String())

    arrive = db.Column(db.DateTime)
    beginexp = db.Column(db.DateTime)
    endexp = db.Column(db.DateTime)
    status = db.Column(db.Integer, default = 1)
    db.datastring = db.Column(db.Text(4294967295))

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.status = "assigned"
        self.arrive = datetime.datetime.now()


    def get_trial_data(self):
        """ Refactor this to use postegresql json functions and reflect actual experiments. 
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
                        self.uniqueid,
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
                    csvwriter.writerow((self.uniqueid, event["eventtype"], event["interval"], event["value"], event["timestamp"]))
                ret = outstring.getvalue()
            return ret
        except:
            print("Error reading record:", self)
            return("")

    def __repr__(self):
        return "Subject(%s, %s, %s, %s)" % ( 
            self.uniqueid, 
            self.status,
            self.codeversion)