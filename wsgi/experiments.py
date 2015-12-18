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

    if not utils.check_qs(request.args, ['uniqueid', 'experimentname']):
        raise ExperimentError('improper_inputs')

    # First check if user is in db, if not add
    # This is independent of finding the specific experiment
    gfg_id = request.args['uniqueid']
    exp_name = request.args['experimentname']
    browser, platform = utils.check_browser_platform(request.user_agent)


    # assert current_app.debug == False
    # Check if user is in db, if not add & commit
    user, new_user = db_utils.get_or_create(db.session, User, gfg_id=gfg_id)

    current_app.logger.info("Subject: %s entered with %s platform and %s browser. New user: %s" %
                            (gfg_id, platform, browser, new_user))

    # If any existing session that disqualify user (ongoing or completed), throw error
    # Otherwise, create new session and serve experiment
    disqualifying_sessions = Session.query.filter((Session.gfg_id == gfg_id) &
                                                  (Session.exp_name == exp_name) &
                                                  ((Session.status == 2) | (Session.status == 3))).all()

    if disqualifying_sessions:
        current_app.logger.info(
            "Found %d sessions in which the user quit early or completed", len(disqualifying_sessions))
        raise ExperimentError('already_did_exp_hit')

    # Otherwise, allow participant to re-enter
    # (Are quit early signals sent back during instruction phase?)
    else:
        session = Session(gfg_id=gfg_id, browser=browser, platform=platform,
                          status=1, exp_name=exp_name, begin_session=datetime.datetime.now())
        db.session.add(session)
        db.session.commit()

        return render_template(exp_name + "/exp.html", uniqueid=gfg_id,
                               experimentname=exp_name, sessionid=session.session_id)


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

    if not utils.check_qs(request.form, ['uniqueid', 'experimentname', 'sessionid']):
        raise ExperimentError('improper_inputs')

    gfg_id = request.form['uniqueid']
    experiment_name = request.form['experimentname']
    session_id = request.form['sessionid']

    session = Session.query.filter((Session.gfg_id == gfg_id) & (
        Session.exp_name == experiment_name) & (Session.session_id == session_id)).first()

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


def parse_id_exp(id_exp):
    resp = None
    try:
        gfg_id, exp_name, session_id = id_exp.split("&")
    except ValueError:
        resp = {"status": "bad request"}
        current_app.logger.error("Could not parse id")
    else:
        try:
            session = Session.query.filter_by(session_id=session_id).one()
        except SQLAlchemyError:
            resp = {"status": "bad request"}
            current_app.logger.error("DB error: Unique user not found.")

    return (gfg_id, exp_name, session_id), session, resp

@experiments.route('/sync/<id_exp>', methods=['GET'])
def load(id_exp=None):
    """
    Return a few attributed of session back to Backbone.js.
    This is forced by Backbone, and doesn't do much.  """

    current_app.logger.info("GET /sync route with id: %s" % id_exp)
    (gfg_id, exp_name, session_id), session, resp = parse_id_exp(id_exp)

    if resp is None:
        # Need to check if we need to send other stuff. Might have to .
        resp = {
            "uniqueid": session.gfg_id,
            "experimentname": session.exp_name,
            "sessionid": session.session_id
        }

    return jsonify(**resp)


@experiments.route('/sync/<id_exp>', methods=['PUT'])
def update(id_exp=None):
    """ Sync backbone model with appropriate database.  """

    current_app.logger.info("PUT /sync route with id: %s" % id_exp)

    (gfg_id, exp_name, session_id), session, resp = parse_id_exp(id_exp)

    # Check JSON validity
    if utils.check_valid_json(request.get_data()):
        valid_json = json.loads(request.get_data())
        # session.datastring = valid_json
    else:
        resp = {"status": "bad request"}
        current_app.logger.error("Invalid JSON")

    current_app.logger.info(
        "Current trial: %s, unique_id: %s, experiment name: %s, session id: %s " % (valid_json['currenttrial'],
            valid_json['uniqueid'], valid_json['experimentname'], valid_json['sessionid']))

    # For each trial, pass to appropriate parser, if not in db
    for json_trial in valid_json['data']:
        if exp_name == "category_switch":
            experiment_class = CategorySwitch
        elif exp_name == "keep_track":
            experiment_class = KeepTrack
        else:
            current_app.logger.error("%s does not exist" % (exp_name))
            resp = {"status": "bad request"}

        db_trial, new = db_utils.get_or_create(db.session,
            experiment_class, gfg_id=gfg_id, session_id=session_id,
            trial_num=json_trial['current_trial'])

        # If the trial is new, add data
        if new:
            db_trial.add_json_data(json_trial)
            db.session.commit()

    # For each event, pass to parser, if not in db
    for json_event in valid_json['eventdata']:
        db_event, new = db_utils.get_or_create(db.session, EventData,
            gfg_id=gfg_id, session_id=session_id, exp_name=exp_name)

        if new:
            db_event.add_json_data(json_event)
            db.session.commit()

    if resp is None:
        resp = {"status": "user data saved"}
    return jsonify(**resp)


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
            db.session.commit()  # Need to add?
            resp = {"status": "marked as quitter"}

        except SQLAlchemyError:
            raise ExperimentError('tried_to_quit')

    return jsonify(**resp)


@experiments.route('/worker_complete', methods=['GET'])
def worker_complete():
    """Complete worker."""

    if not utils.check_qs(request.args, ['sessionid', 'uniqueid']):
        raise ExperimentError('improper_inputs')
    else:
        session_id = request.args['sessionid']
        gfg_id = request.args['uniqueid']
        current_app.logger.info(
            "Completed experiment %s" % (session_id))
        try:
            # pull records from Session table to update
            session = Session.query.filter(
                Session.session_id == session_id).one()
            session.status = 3
            db.session.commit()

        except SQLAlchemyError:
            raise ExperimentError('unknown_error')

        # This needs to be updated because I'm not sure where to route when all
        # is done.
        return redirect(url_for(".index", uniqueid=gfg_id, new=False))


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
