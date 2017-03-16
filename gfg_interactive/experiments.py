from flask import Blueprint, render_template, request, jsonify, current_app, url_for, redirect
from errors import ExperimentError
from models import Session, Participant, CategorySwitch, EventData, KeepTrack, QuestionData, BART
from sqlalchemy import func, asc, distinct
from sqlalchemy.exc import SQLAlchemyError
from database import db
import db_utils
import datetime
import json
import urllib
import utils
import stats

# Status codes
NOT_ACCEPTED = 0
ALLOCATED = 1
STARTED = 2
COMPLETED = 3
QUITEARLY = 6


### JAKE: this sets up where this file looks for the templates and static
experiments = Blueprint('experiments', __name__,
                        template_folder='exp/templates', static_folder='exp/static')

### JAKE: here you would need to pair a surveyid number (e.g. 30), and a name for your task "bart"
experiment_list = {'28': 'keep_track', '29' : 'category_switch', '30' : 'BART'}

@experiments.route('/', methods=['GET'])
def index():
    """ Welcome page, but there is none so right now its blank"""
    return render_template("default.html")

@experiments.route('/task', methods=['GET'])
@utils.nocache
def start_exp():
    """ Serves up the experiment applet.
    If experiment is ongoing or completed, will not serve.

    Querystring args (required):
    uniqueid: External gfg_id
    surveyid: Which experiment to serve
    """

    browser, platform = utils.check_browser_platform(request.user_agent)

    # Check query string
    if not utils.check_qs(request.args, ['uniqueid', 'surveyid']):
        raise ExperimentError('improper_inputs')
    else:
        uniqueid = request.args['uniqueid']
        survey_id = request.args['surveyid']
        exp_name = experiment_list[request.args['surveyid']] # Survey id to experiment name

    # Decrypt encocded uniqueid
    gfg_id = utils.decrypt(str(current_app.config['SECRET_KEY']), str(uniqueid).decode('string-escape'))

    # Check if user exists in main gfg db
    if not db_utils.gfg_user_exists(gfg_id, current_app.config['RESEARCH_DB_HOST'],
     current_app.config['RESEARCH_DB_USER'],
        current_app.config['RESEARCH_DB_PASSWORD'], current_app.config['RESEARCH_DB_NAME']):
        raise ExperimentError('user_access_denied')

    # Check if user is in Participant table, if not add & commit
    user, new_user = db_utils.get_or_create(db.session, Participant, gfg_id=gfg_id)

    current_app.logger.info("Subject: %s entered with %s platform and %s browser" %
                            (gfg_id, platform, browser))

    # If any existing sessions disqualify user (ongoing or completed), throw error
    # Otherwise, create new session and serve experiment
    disqualifying_sessions = Session.query.filter_by(gfg_id = gfg_id, exp_name = exp_name, status = 3).first()
    if disqualifying_sessions and current_app.config['EXP_DEBUG'] == False and exp_name != 'BART':
        raise ExperimentError('already_did_exp', session_id=disqualifying_sessions.session_id)

    # Otherwise, allow participant to re-enter
    else:
        session = Session(gfg_id=gfg_id, browser=browser, platform=platform,
                          status=1, exp_name=exp_name, begin_session=datetime.datetime.now())
        db.session.add(session)
        db.session.commit()

        return render_template(exp_name + "/exp.html", experimentname=exp_name, surveyid=survey_id,
            sessionid=session.session_id, debug=current_app.config['EXP_DEBUG'],
            uniqueid=urllib.quote(uniqueid))

### JAKE: this function is called by dataHandler.finishInstructions()
@experiments.route('/inexp', methods=['POST'])
def enterexp():
    """
    AJAX listener that listens for a signal from the user's script when they
    leave the instructions and enter the real experiment. After the server
    receives this signal, it will no longer allow them to re-access the
    experiment applet (meaning they can't do part of the experiment and
    refresh to start over). This changes the current sessions's status to 2.

    Querystring args (required):
    uniqueid: External gfg_id
    experimentname: Which experiment to serve
    sessionid: session identifier
    """

    if not utils.check_qs(request.form, ['sessionid']):
        raise ExperimentError('improper_inputs')
    else:
        session_id = request.form['sessionid']

    session = Session.query.filter_by(session_id=session_id).first()

    if session:
        session.status = 2
        session.begin_experiment = datetime.datetime.now()
        db.session.commit()

        current_app.logger.info(
            "User has finished the instructions in session id: %s, experiment name: %s",
            session_id, session.exp_name)
        resp = {"status": "success"}
    else:
        current_app.logger.error(
            "DB error: Unique user and experiment combination not found.")
        # it is the dictionary
        resp = {"status": "error, session not found"}

    return jsonify(**resp)


@experiments.route('/sync/<session_id>', methods=['GET'])
def load(session_id=None):
    """
    Return a few attributed of session back to Backbone.js.
    This is forced by Backbone, and doesn't do much.  """

    current_app.logger.info("GET /sync route with id: %s" % session_id)
    try:
        session = Session.query.filter_by(session_id=session_id).one()
    except SQLAlchemyError:
        resp = {"status": "bad request"}
        current_app.logger.error("DB error: Unique user not found.")
    else:
        resp = {
            "sessionid": session.session_id
        }

    return jsonify(**resp)


@experiments.route('/sync/<session_id>', methods=['PUT'])
def update(session_id=None):
    """ Sync backbone model with appropriate database.  """

    current_app.logger.info("PUT /sync route with id: %s" % session_id)
    resp = None

    try:
        session = Session.query.filter_by(session_id=session_id).one()
    except SQLAlchemyError:
        resp = {"status": "bad request"}
        current_app.logger.error("DB error: Unique user not found.")

    # Check JSON validity
    if utils.check_valid_json(request.get_data()):
        valid_json = json.loads(request.get_data())
    else:
        resp = {"status": "bad request"}
        current_app.logger.error("Invalid JSON")

    current_app.logger.info(
        "Current trial: %s, session id: %s " % (valid_json['currenttrial'],
            valid_json['sessionid']))

    ## JAKE: This needs to be slightly customized to add your task
    ## However, most of the work will be in models.py
    # For each trial, pass to appropriate parser, if not in db
    for json_trial in valid_json['data']:
        if session.exp_name == "category_switch":
            experiment_class = CategorySwitch
        elif session.exp_name == "keep_track":
            experiment_class = KeepTrack
        elif session.exp_name == 'BART':
            experiment_class = BART

        db_trial, new = db_utils.get_or_create(db.session,
            experiment_class, gfg_id=session.gfg_id, session_id=session.session_id,
            trial_num=json_trial['current_trial'])

        # If the trial is new, add data
        if new:
            db_trial.add_json_data(json_trial)
            db.session.commit()

    ## JAKE: this part is for recording events that dataHandler (i.e. psiTurk),
    ## tracks, automatically
    # For each event, pass to parser, if not in db
    for json_event in valid_json['eventdata']:
        db_event, new = db_utils.get_or_create(db.session, EventData,
            gfg_id=session.gfg_id, session_id=session.session_id, exp_name=session.exp_name,
            timestamp = utils.convert_timestamp(json_event['timestamp']))

        if new:
            db_event.add_json_data(json_event)
            db.session.commit()

    ## JAKE: Don't worry about this now, you won't have any question data
    if valid_json['questiondata'] != {}:
        # For the QuestionData, pass to parser, if not in db
        db_ques, new = db_utils.get_or_create(db.session, QuestionData,
                    gfg_id=session.gfg_id, session_id=session.session_id, exp_name=session.exp_name)
        db_ques.add_json_data(valid_json['questiondata'])
        db.session.commit()

    if resp is None:
        resp = {"status": "success"}

    return jsonify(**resp)

## JAKE: If someone quits, this is called by dataHandler
@experiments.route('/quitter', methods=['POST'])
def quitter():
    """ Mark quitter as such. """
    if not utils.check_qs(request.form, ['sessionid']):
        resp = {"status": "bad request"}

    else:
        session_id = request.form['sessionid']

        try:
            # pull records from Session table to update
            session = Session.query.filter(
                Session.session_id == session_id).one()
            session.status = 6
            db.session.commit()
            resp = {"status": "marked as quitter"}

        except SQLAlchemyError:
            resp = {"status": "bad request"}

    return jsonify(**resp)

## JAKE: this is called by dataHandler.completeTask()
@experiments.route('/worker_complete', methods=['POST'])
def worker_complete():
    """Complete worker."""

    if not utils.check_qs(request.form, ['sessionid']):
        resp = {"status": "bad request"}
    else:
        session_id = request.form['sessionid']
        current_app.logger.info(
            "Completed experiment %s" % (session_id))
        try:
            # pull records from Session table to update
            session = Session.query.filter(
                Session.session_id == session_id).one()
            session.status = 3
            db.session.commit()
            resp = {"status": "marked as done"}
            current_app.logger.info("Subject: %s marked as done" %
                        str(session.gfg_id))

        except SQLAlchemyError:
            raise ExperimentError('unknown_error', session_id=request.args['sessionid'])
            resp = {"status": "db error"}

        return jsonify(**resp)

## As you know, this is where you  get routed for results
@experiments.route('/results', methods=['GET'])
def results():
    """Return results at the end."""
    if not utils.check_qs(request.args, ['uniqueid','surveyid']):
        raise ExperimentError('improper_inputs')
    else:
        uniqueid = request.args['uniqueid']
        survey_id = request.args['surveyid']
        exp_name = experiment_list[request.args['surveyid']]

    current_app.logger.info("Results: uniqueid is  %s, exp_name is %s and survey id is %s" %(uniqueid, exp_name, survey_id))
    ## Get last session with code 3 from user

    gfg_id = utils.decrypt(str(current_app.config['SECRET_KEY']), str(uniqueid))
    current_app.logger.info("GFG id after decrypt is -- %s" % (gfg_id))

    # I would leave all the stuff above alone, as its just getting all the variable it needs

    # Here we are "supposedly" querying the DB for the last session from that user. it is possible that this should be asc() not desc()
    try:
        session = Session.query.filter_by(gfg_id=gfg_id, status=3, exp_name=exp_name).order_by(Session.session_id.desc()).first()
    except SQLAlchemyError:
        raise ExperimentError('user_access_denied')

    # As you can see, we start doing things different for each task here, but template is still just
    # expecting two variables, score and percentile (last line). So if you want to do something
    # totally different, then you need to stick an if statement that splits off the whole thing here
    # if session.exp_name == "bart": {your stuff} else:
    if session is None :
    	current_app.logger.info("Session is null---%s" %(session))
    	raise ExperimentError('user_access_denied')

    elif session.exp_name == "keep_track":
        target_trials = KeepTrack.query.filter(KeepTrack.session_id==session.session_id,
            KeepTrack.block.in_(["1", "2", "3", "4", "5", "6"])).all()

        all_scored = []
        for trial in target_trials:
            score = trial.simple_score()
            all_scored += score
            current_app.logger.info("trial score: %s, block: %s, inwords: %s" % (str(score), trial.block, str(trial.input_words)))

        ## This first value should be stored
        score = sum(all_scored) / (len(all_scored)  * 1.0)

    elif session.exp_name == "category_switch":
        single_trials_avg = db.session.query(func.avg(CategorySwitch.reaction_time).label('average')).filter(
            CategorySwitch.session_id==session.session_id, CategorySwitch.block.in_(["sizeReal", "livingReal"]),
                CategorySwitch.accuracy==1).all()
        mixed_trials_avg = db.session.query(func.avg(CategorySwitch.reaction_time).label('average')).filter(
            CategorySwitch.session_id==session.session_id, CategorySwitch.block.in_(["mixedReal1", "mixedReal2"]),
                CategorySwitch.accuracy==1).all()

        ## This value also needs to be stored
        score = mixed_trials_avg[0][0] - single_trials_avg[0][0]

    ## JAKE: You'd need to add another elif for your task. This is probably not the best way to code this but oh well
    ## Probably would be good to have the scoring functions all in one file and just call the right function for the git
    ## task, but lets leave that for later
    elif session.exp_name == 'BART':

        # Individuals previous scores
        previousSessions = [_[0] for _ in db.session.query(Session.results).filter(Session.gfg_id == gfg_id,
                                               Session.exp_name == exp_name,
                                               Session.session_id != session.session_id,
                                               Session.status == 3).order_by(asc(Session.session_id)).all()]

        if len(previousSessions) == 0:
            previousSessions = None


        # current score
        score = round(db.session.query(func.avg(BART.pumps).label('average')).filter(BART.session_id == session.session_id,
                                                                               BART.user_action == 1).all()[0][0])
        session.results = score
        db.session.commit()
        print score

        # data from subjects with completed sessions
        completed_others = [_[0] for _ in db.session.query(distinct(Session.gfg_id)).filter(
                                               # Session.gfg_id != gfg_id,
                                               Session.exp_name == session.exp_name,
                                               Session.status == 3).all()]

        if len(completed_others) > 0:

            mean_score = db.session.query(func.avg(Session.results).label('average')).filter(
                Session.gfg_id.in_(completed_others),
                Session.status == 3,
                Session.exp_name == exp_name).group_by(Session.gfg_id).all()

            std_score = db.session.query(func.STD(Session.results).label('average')).filter(
                Session.gfg_id.in_(completed_others),
                Session.status == 3,
                Session.exp_name == exp_name).group_by(Session.gfg_id).all()

            percentile = stats.z2p((score - mean_score[0][0]) / (std_score[0][0] + 0.0000001))
            otherResults = [_[0] for _ in db.session.query(Session.results).filter(Session.gfg_id.in_(completed_others),
                                                                                   Session.status == 3,
                                                                                   Session.exp_name == exp_name).all()]
        else:
            percentile = None
            otherResults = None

        return render_template(session.exp_name + "/results.html",
                               score=score,
                               others = otherResults,
                               previousSessions = previousSessions,
                               percentile = percentile
                               )

    # Do make sure to save the value that you computer for each subject here
    session.results = score
    db.session.commit()

    ## I would also make sure to use the same method to get "comparion subjects"
    ## to have consistency across GFG

    ## Find other people in same age range. If more than 20, calculate percentile and display
    age_matched_ids = db_utils.get_age_matched_ids(gfg_id, current_app.config['RESEARCH_DB_HOST'], current_app.config['RESEARCH_DB_USER'],
    current_app.config['RESEARCH_DB_PASSWORD'], current_app.config['RESEARCH_DB_NAME'])

    # Importantly, I only show results if I have at least 20 control subjects, so when there is very little data
    # I don't show anything because it can be misleading.
    if len(age_matched_ids) > 20:
        mean_score = db.session.query(func.avg(Session.results).label('average')).filter(
        Session.gfg_id.in_(age_matched_ids), Session.exp_name == session.exp_name, Session.status==3).all()

        std_score = db.session.query(func.STD(Session.results).label('average')).filter(
        Session.gfg_id.in_(age_matched_ids), Session.exp_name == session.exp_name, Session.status==3).all()


        percentile = stats.z2p((score - mean_score[0][0]) / (std_score[0][0] + 0.0000001))
    else:
        percentile = None

    # If you're going to do something different, then you'd want this call to be in your own
    # "if" branch, because presumable you'd want to pass different variables. 
    return render_template(session.exp_name + "/results.html",
        score=score,
        percentile=percentile)


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
    return exception.error_page(request, "gfgemail@gfg.edu") ## Update this email
