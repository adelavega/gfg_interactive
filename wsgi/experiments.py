from flask import Blueprint, render_template, request, jsonify, current_app, url_for, redirect
from utils import nocache
from errors import ExperimentError
from models import Session, User, CategorySwitch, EventData, KeepTrack

from sqlalchemy.exc import SQLAlchemyError
from database import db
import db_utils
import datetime
import json

import utils

# Status codes
NOT_ACCEPTED = 0
ALLOCATED = 1       # given when the user has entered the instructions phase
# given when the user has entered the actual experiment (and at this point
# the trials need to be recorded )
STARTED = 2
COMPLETED = 3
QUITEARLY = 6

experiments = Blueprint('experiments', __name__,
                        template_folder='exp/templates', static_folder='exp/static')

experiment_list = [
    ('keep_track', "Keep Track"), ('category_switch', "Category Switch")]


@experiments.route('/', methods=['GET'])
def index():
    """ Welcome page, but there is none so right now its blank"""
    return render_template("begin.html")


@experiments.route('/task', methods=['GET'])
@nocache
def start_exp():
    """ Serves up the experiment applet. 
    If experiment is ongoing or completed, will not serve. 

    Querystring args (required):
    uniqueid: External gfg_id
    experimentname: Which experiment to serve
    """

    if not utils.check_qs(request.args, ['uniqueId', 'experimentName']):
        raise ExperimentError('improper_inputs')

    # First check if user is in db, if not add
    # This is independent of finding the specific experiment
    unique_id = request.args['uniqueId']
    exp_name = request.args['experimentName']
    browser, platform = utils.check_browser_platform(request.user_agent)

    # Check if user is in db, if not add & commit
    user, new_user = db_utils.get_or_create(db.session, User, gfg_id=unique_id)

    current_app.logger.info("Subject: %s entered with %s platform and %s browser. New: %s" %
                            (unique_id, platform, browser, new_user))

    # If any existing session that disqualify user (ongoing or completed), throw error
    # Otherwise, create new session and serve experiment
    disqualifying_sessions = Session.query.filter((Session.gfg_id == unique_id) &
                                                  (Session.exp_name == exp_name) &
                                                  ((Session.status == 2) | (Session.status == 3))).all()

    if disqualifying_sessions:
        current_app.logger.info(
            "Found %d sessions in which the user quit early or completed", len(disqualifying_sessions))
        raise ExperimentError('already_did_exp_hit')

    # Otherwise, allow participant to re-enter
    # (Are quit early signals sent back during instruction phase?)
    else:
        session = Session(gfg_id=unique_id, browser=browser, platform=platform,
                       status=1, exp_name=exp_name, begin_session=datetime.datetime.now())
        db.session.add(session)
        db.session.commit()

        return render_template(exp_name + "/exp.html", uniqueId=unique_id,
                               experimentName=exp_name, sessionid=session.session_id)


@experiments.route('/inexp', methods=['POST'])
def enterexp():
    """
    AJAX listener that listens for a signal from the user's script when they
    leave the instructions and enter the real experiment. After the server
    receives this signal, it will no longer allow them to re-access the
    experiment applet (meaning they can't do part of the experiment and
    refresh to start over). This changes the current sessions's status to 2.
    """

    if not utils.check_qs(request.form, ['uniqueId', 'experimentName', 'sessionid']):
        raise ExperimentError('improper_inputs')

    unique_id = request.form['uniqueId']
    experiment_name = request.form['experimentName']
    session_id = request.form['sessionid']  # Change to use same case

    session = Session.query.filter((Session.gfg_id == unique_id) & (
            Session.exp_name == experiment_name) & (Session.session_id == session_id)).first()

    if session:
        session.status = 2
        db.session.commit()

        current_app.logger.info(
            "User has finished the instructions in session id: %s, experiment name: %s", session_id, session.exp_name)
        resp = {"status": "success"}
    else:
        current_app.logger.error(
            "DB error: Unique user and experiment combination not found.")
        # it is the dictionary
        resp = {"status": "error, session not found"}

    return jsonify(**resp)


# called to retrieve the JSON object for returning users
@experiments.route('/sync/<id_exp>', methods=['GET'])
def load(id_exp=None):
    """
    Load experiment data, which should be a JSON object and will be storedafter converting to string """

    current_app.logger.info("GET /sync route with id: %s" % id_exp)
    try:
        unique_id, experiment_name, session_id = id_exp.split("&")

        # Do we need to call. one()? Or shouldn't that be implied there's only
        # one session?
        session = Session.query.filter((Session.gfg_id == unique_id) & (
            Session.exp_name == experiment_name) & (Session.session_id == session_id)).one()
    except SQLAlchemyError:
        current_app.logger.error(
            "DB error: Unique user /experiment combo not found.")

    # What's going on here?
    # I kinda forgot what the get function was for... I think it's rarely used
    # in practice

    # lets try to find all the session ids associated with the unique_id &
    # exp_name combo
    session_id_list = []
    if experiment_name == "category_switch":
        records = CategorySwitch.query.filter(
            (CategorySwitch.gfg_id == unique_id)).all()
        for r in records:
            if r.sess_id in session_id_list:
                print "in list, dont add"
            else:
                session_id_list = session_id_list + [r.sess_id]
    elif experiment_name == "keep_track":
        print "you gotta query keeptrack"
        records = KeepTrack.query.filter(
            (KeepTrack.gfg_id == unique_id)).all()
        for r in records:
            if r.sess_id in session_id_list:
                print "in list, dont add"
            else:
                session_id_list = session_id_list + [r.sess_id]
    else:
        print "table name incorrect/not found"

    current_app.logger.info("%s session ids associated with %s unique_id for %s experiment" % (
        session_id_list, unique_id, experiment_name))
    try:
        resp = json.loads(user.datastring)
    except:
        resp = {
            "uniqueId": user.gfg_id,
            "experimentName": user.experimentname,
            "sessionid": session.session_id
        }
    return jsonify(**resp)


# called to updated the JSON everytime and push it back to the table
@experiments.route('/sync/<id_exp>', methods=['PUT'])
def update(id_exp=None):
    """
    Save experiment data, which should be a JSON object and will be stored after converting to string. """

    current_app.logger.info("PUT /sync route with id: %s" % id_exp)
    unique_id, experiment_name, session_id = id_exp.split("&")

    try:
        Session.query.filter((Session.gfg_id == unique_id) & (
            Session.exp_name == experiment_name) & (Session.session_id == session_id)).one()
    except SQLAlchemyError:
        current_app.logger.error("DB error: Unique user not found.")

    # 1. get the JSON from the request
    if hasattr(request, 'json'):
        datastring = request.get_data().decode(
            'utf-8').encode('ascii', 'xmlcharrefreplace')  # encoding the json

    # 3.Now try to load the "datastring" from the participant table
    try:
        data = json.loads(datastring)
    except:
        data = {}

    # 4. Now extract the latest trial from this freshly saved data
    trial = data.get("currenttrial", None)
    # print "trial is - ", trial
    current_app.logger.info("Saved Trial data for %s, experiment %s and trial# %s in Participant table" % (
        unique_id, experiment_name, trial))

    # 5. Now we will parse the recieved jSON and store each trial in the
    # Category_Switch table

    # Can we do this once? And save into a variable?
    jsont = request.get_data()
    json_obj = json.dumps(jsont)

    # 6. Check if the json is valid
    try:
        json.loads(json_obj)
    except ValueError, e:
        print "Not valid"
        # throw an error here and return out TBD

    # Why the dumps? and loads?
    valid_json = json.loads(jsont)
   # test code
    print "------------------- JSON PARSING Begins here -----------------------------"
    print "currenttrial of JSON :", valid_json['currenttrial']
    print "unique id  of JSON :", valid_json['uniqueId']
    print "Experiment Name of JSON :", valid_json['experimentName']
    print "session id  of JSON :", valid_json['sessionid']

    s = valid_json['sessionid']

    # I'm not sure if we need to worry about these fringe cases too much
    # 7. Extract session_id, experiment_name, uniqueid from JSON and compare
    # it with request data
    if unique_id != valid_json['uniqueId']:
        print "Unique ID in request and jSON not matching. Create an error code for this one."
        # throw an error here and return out TBD
    elif int(session_id) != int(s):
        print "session_id ", session_id
        print "valid_json['sessionid'] ", s
        print "Session ID in request and jSON not matching. Create an error code for this one."
        # throw an error here and return out TBD
    elif experiment_name != valid_json['experimentName']:
        print "Experiment Name in request and jSON not matching. Create an error code for this one."
        # throw an error here and return out TBD
    else:
        current_app.logger.info(
            "Log 013 - All the ids match between JSON and request")

    # 8. Query the appropriate table based on experiment name
    # Separate each task to their own function

    if valid_json['experimentName'] == "category_switch":
        # Query CategorySwitch table
        # Add all the trial numbers pertaining to that session id, unique_id
        # combo into an array
        current_app.logger.info(
            "Querying %s table" % valid_json['experimentName'])
        row_matches = CategorySwitch.query.filter(
            (CategorySwitch.gfg_id == unique_id) & (CategorySwitch.sess_id == session_id)).all()
        trial_list = []
        for r in row_matches:
            trial_list = trial_list + [r.trial_num]
        current_app.logger.info(
            "Log 014 - %s trials found for sessionid %s" % (trial_list, valid_json['sessionid']))
        print "Parsing the JSON CS..........."
        for d in valid_json['data']:
            if d['current_trial'] in trial_list:
                rec = CategorySwitch.query.filter((CategorySwitch.gfg_id == unique_id) & (
                    CategorySwitch.sess_id == session_id) & (CategorySwitch.trial_num == d['current_trial'])).one()
                td = d['trialdata']
                if rec.response == td['resp']:
                    if rec.accuracy == td['acc']:
                        print "Record already exists"
                else:
                    print "Record exists but data seems different"
            else:
                td = d['trialdata']
                # Special case for accuracy
                if td['acc'] == "FORWARD":
                    # numeric denotation of 'FORWARD' can be changed. TBD
                    acc = 11
                elif td['acc'] == "BACK":
                    acc = 22
                elif td['acc'] == "NA":
                    acc = 99
                else:
                    acc = td['acc']
                # Special case for reaction time
                if td['rt'] == "NA":
                    rt = 0
                else:
                    rt = td['rt']
                # Datetime conversion
                jsts = d['dateTime']  # Javscript timestamp
                dt = datetime.datetime.fromtimestamp(jsts/1000.0)
                # Block conversion
                block2 = td['block']
                # need to replace special chars like - /, ',
                block1 = block2.replace("\t", "").replace(
                    "\n", "").replace("'", "")
                cs_info_trial = CategorySwitch(gfg_id=unique_id, sess_id=session_id, trial_num=d['current_trial'], response=td[
                    'resp'], reaction_time=rt, accuracy=acc, block=block1, question="null",
                    answer="null", user_answer="null", beginexp=dt)
                db.session.add(cs_info_trial)
                db.session.commit()
                current_app.logger.info(
                    "Log 015 - %s added to Category_Switch for session id %s " % (d['current_trial'], session_id))

    elif valid_json['experimentName'] == "keep_track":
        current_app.logger.info(
            "Querying %s table" % valid_json['experimentName'])
        row_matches = KeepTrack.query.filter(
            (KeepTrack.gfg_id == unique_id) & (KeepTrack.sess_id == session_id)).all()
        trial_list = []
        for r in row_matches:
            trial_list = trial_list + [r.trial_num]
        current_app.logger.info(
            "Log 016 - %s trials found for sessionid %s" % (trial_list, valid_json['sessionid']))
        print "Parsing the JSON KT..........."
        for d in valid_json['data']:
            if d['current_trial'] in trial_list:
                print "Record already exists"
            else:  # trial not already in table so add it
                td = d['trialdata']
                tw1 = tw2 = tw3 = tw4 = tw4 = tw5 = "null"  # Target words
                iw1 = iw2 = iw3 = iw4 = iw4 = iw5 = "null"  # Input words
                if 'rt' not in td:
                    rt = 99.99
                else:
                    rt = td['rt']
                    print "Rt is ", rt
                if 'acc' not in td:
                    acc = "null"
                else:
                    acc = td['acc']
                if 'target_words' not in td:
                    print " no target words"
                else:
                    length = len(td['target_words'])
                    if length == 3:
                        tw1 = td['target_words'][0]
                        tw2 = td['target_words'][1]
                        tw3 = td['target_words'][2]
                    if length == 4:
                        tw1 = td['target_words'][0]
                        tw2 = td['target_words'][1]
                        tw3 = td['target_words'][2]
                        tw4 = td['target_words'][3]
                    if length == 5:
                        tw1 = td['target_words'][0]
                        tw2 = td['target_words'][1]
                        tw3 = td['target_words'][2]
                        tw4 = td['target_words'][3]
                        tw5 = td['target_words'][4]
                if 'input_words' not in td:
                    print "no input words"
                else:
                    length = len(td['input_words'])
                    if length == 3:
                        iw1 = td['input_words'][0]
                        iw2 = td['input_words'][1]
                        iw3 = td['input_words'][2]
                    if length == 4:
                        iw1 = td['input_words'][0]
                        iw2 = td['input_words'][1]
                        iw3 = td['input_words'][2]
                        iw4 = td['input_words'][3]
                    if length == 5:
                        iw1 = td['input_words'][0]
                        iw2 = td['input_words'][1]
                        iw3 = td['input_words'][2]
                        iw4 = td['input_words'][3]
                        iw5 = td['input_words'][4]
                # Datetime conversion
                jsts = d['dateTime']  # Javscript timestamp
                dt = datetime.datetime.fromtimestamp(jsts/1000.0)
                # Block conversion
                block2 = td['block']
                # need to replace special chars like - /, ',
                block1 = block2.replace("\t", "").replace(
                    "\n", "").replace("'", "")
                kt_info_trial = KeepTrack(gfg_id=unique_id, sess_id=session_id, trial_num=d['current_trial'],
                                          reaction_time=rt, accuracy=acc, block=block1, beginexp=dt, target_word1=tw1,
                                          target_word2=tw2, target_word3=tw3, target_word4=tw4, target_word5=tw5,
                                          input_word1=iw1, input_word2=iw2, input_word3=iw3, input_word4=iw4, input_word5=iw5)
                db.session.add(kt_info_trial)
                db.session.commit()
                current_app.logger.info(
                    "Log 017 - %s added to Keep Track for session id %s " % (d['current_trial'], session_id))
                print "++++++++++++++++++++++++++++++"
    else:
        current_app.logger.info(
            "Log 018 - %s not found in database" % (valid_json['experimentName']))
        # throw an error here and return out TBD

    # Populate EventData Table
    # Separate into own function
    # I think these function should be attached to the datamodel int models.py
    # list to store the timestamps of all the events in the table
    event_list = []
    current_app.logger.info("Log 019 - Querying Event_data table")
    e_matches = EventData.query.filter((EventData.gfg_id == unique_id) & (
        EventData.sess_id == session_id) & (EventData.exp_name == experiment_name)).all()
    for row in e_matches:
        # row.timestamp will be in datetime format.
        event_list = event_list + [row.timestamp]

    for e in valid_json['eventdata']:
        val1 = "null"
        val2 = "null"
        val3 = "null"
        print "event type: ", e['eventtype']
        # convert timestamp to datetime format and then check in the list if it
        # exists
        jstime = e['timestamp']
        dtime = datetime.datetime.fromtimestamp(jstime/1000.0)
        if dtime in event_list:
            print "Event already addded"
        else:   # Add the event to the table
            if isinstance(e['value'], list):
                val1 = str(e['value'][0])
                val2 = str(e['value'][1])
            else:
                val3 = str(e['value'])
            e_trial = EventData(gfg_id=unique_id, sess_id=session_id, exp_name=experiment_name, event_type=e[
                'eventtype'], interval=e['interval'], timestamp=dtime, value_1=val1, value_2=val2, value_3=val3)
            db.session.add(e_trial)
            db.session.commit()
            current_app.logger.info(
                "Log 018 - %s added to Event_data for session id %s " % (e['eventtype'], session_id))

    resp = {"status": "user data saved"}
    return jsonify(**resp)


@experiments.route('/quitter', methods=['POST'])
def quitter():
    """ Mark quitter as such. """
    if not ('uniqueId' in request.form) or not ('experimentName' in request.form) or not ('sessionid' in request.form):
        resp = {"status": "bad request"}
        return jsonify(**resp)

    unique_id = request.form['uniqueId']
    experiment_name = request.form['experimentName']
    session_id = request.form['sessionid']

    if unique_id[:5] == "debug":
        debug_mode = True
    else:
        debug_mode = False

    """if debug_mode:
        resp = {"status": "didn't mark as quitter since this is debugging"}
        return jsonify(**resp)
    else:"""
    try:
        # pull records from Session table to update
        session = Session.query.filter((Session.gfg_id == unique_id) & (
            Session.exp_name == experiment_name) & (Session.session_id == session_id)).one()
        print "** session: ", session
        session.status = 6

        # Again I'm not sure its appropriate to do this since this is not the
        # true start
        session.begin_session = datetime.datetime.now()
        db.session.add(session)
        db.session.commit()

    except SQLAlchemyError:
        raise ExperimentError('tried_to_quit')
    else:
        resp = {"status": "marked as quitter"}
        return jsonify(**resp)


@experiments.route('/worker_complete', methods=['GET'])
def worker_complete():
    """Complete worker."""

    if 'debug' in request.args:
        debug = request.args['debug']
    else:
        debug = False

    if not ('uniqueId' in request.args) or not ('experimentName' in request.args) or not ('sessionid' in request.args):
        raise ExperimentError('improper_inputs')

    else:
        unique_id = request.args['uniqueId']
        experiment_name = request.args['experimentName']
        session_id = request.args['sessionid']
        current_app.logger.info(
            "Completed experiment %s, %s, %s" % (unique_id, experiment_name, session_id))
        try:
            # pull records from Session table to update
            session = Session.query.filter((Session.gfg_id == unique_id) & (
                Session.exp_name == experiment_name) & (Session.session_id == session_id)).one()
            print "** session: ", session
            session.status = 3

            # Again not sure if we need to do this
            session.begin_session = datetime.datetime.now()
            db.session.add(session)
            db.session.commit()

        except SQLAlchemyError:
            raise ExperimentError('unknown_error')

        return redirect(url_for(".index", uniqueId=unique_id, new=False, debug=debug))


# Generic route
@experiments.route('/<pagename>')
@experiments.route('/<foldername>/<pagename>')
def regularpage(foldername=None, pagename=None):
    """
    Route not found by the other routes above. May point to a static template.
    """
    from jinja2.exceptions import TemplateNotFound

    try:

        if foldername is None and pagename is not None:
            return render_template(pagename)
        else:
            return render_template(foldername+"/"+pagename)
    except TemplateNotFound:
        return render_template("error.html", errornum=404)


@experiments.errorhandler(ExperimentError)
def handle_exp_error(exception):
    """Handle errors by sending an error page."""
    current_app.logger.error(
        "%s (%s) %s", exception.value, exception.errornum, str(dict(request.args)))
    return exception.error_page(request, "delavega@colorado.edu")
