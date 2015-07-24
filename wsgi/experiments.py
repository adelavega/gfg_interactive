from flask import Blueprint, render_template, request, jsonify, current_app
from utils import nocache
from errors import ExperimentError
from models import Participant

from sqlalchemy.exc import SQLAlchemyError
from database import db

import datetime
import json

# Status codes
NOT_ACCEPTED = 0
ALLOCATED = 1
STARTED = 2
COMPLETED = 3
QUITEARLY = 6

experiments = Blueprint('experiments', __name__,
                        template_folder='exp/templates', static_folder='exp/static')

experiment_list = [('keep_track', "Keep Track"), ('category_switch', "Category Switch")]

@experiments.route('/', methods=['GET'])
def welcome():
    """ Serves welcome page, sets up data base, and forwards to experiment if ready"""

    if not ('uniqueId' in request.args):
        raise ExperimentError('hit_assign_worker_id_not_set_in_exp')

    if 'debug' in request.args:
        debug = request.args['debug']
    else:
        debug = False

    if 'new' in request.args:
        new = bool(int(request.args['new']))
    else:
        new = True 

    unique_id = request.args['uniqueId']

    current_app.logger.info("Subject: %s arrived" % unique_id)

    # Check to see which if any experiments this subject has done
    matches = Participant.query.\
        filter((Participant.uniqueid == unique_id) & (Participant.status > 1)).\
        all()

    experiments_left = [exp for exp in experiment_list if exp[0] not in [match.experimentname for match in matches]]

    return render_template("begin.html", uniqueId=unique_id, experiments=experiments_left, debug=debug, new=new)

@experiments.route('/task', methods=['GET'])
@nocache
def start_exp():
    """ Serves up the experiment applet. """


    if not ('uniqueId' in request.args):
        raise ExperimentError('hit_assign_worker_id_not_set_in_exp')
    elif not ('experimentName' in request.args) or not (request.args['experimentName'] in zip(*experiment_list)[0]):
        raise ExperimentError('experiment_code_error')

    if 'debug' in request.args:
        debug = request.args['debug']
        debug = debug == 'True'
    else:
        debug = False


    unique_id = request.args['uniqueId']
    experiment_name = request.args['experimentName']

    current_app.logger.info("Subject: %s in task %s" % (unique_id, experiment_name))


      # Check to see which if any experiments this subject has done
    matches = Participant.query.\
        filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).\
        all()


    numrecs = len(matches)

    if numrecs == 0:
        # Choose condition and counterbalance

        worker_ip = "UNKNOWN" if not request.remote_addr else \
            request.remote_addr
        browser = "UNKNOWN" if not request.user_agent.browser else \
            request.user_agent.browser
        platform = "UNKNOWN" if not request.user_agent.platform else \
            request.user_agent.platform
        language = "UNKNOWN" if not request.user_agent.language else \
            request.user_agent.language

        part = Participant(uniqueid=unique_id, ipaddress=worker_ip, browser=browser, platform=platform,
            language=language, experimentname=experiment_name, debug=debug)

        db.session.add(part)
        db.session.commit()

    elif numrecs > 0:
        # They've already done an assignment, then we should tell them they
        #    can't do another one

        part = matches[0]
        current_app.logger.info(part)

        ## Status
        if int(part.status) > 1 and debug == False:
            raise ExperimentError('already_started_exp')

        
    return render_template(experiment_name + "/exp.html", uniqueId=unique_id, experimentName=experiment_name)


@experiments.route('/inexp', methods=['POST'])
def enterexp():
    """
    AJAX listener that listens for a signal from the user's script when they
    leave the instructions and enter the real experiment. After the server
    receives this signal, it will no longer allow them to re-access the
    experiment applet (meaning they can't do part of the experiment and
    referesh to start over).
    """

    if not ('uniqueId' in request.form) or not ('experimentName' in request.form):
        raise ExperimentError('improper_inputs')

    unique_id = request.form['uniqueId']
    experiment_name = request.form['experimentName']

    try:
        user = Participant.query.\
            filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).one()
        user.status = 2
        user.beginexp = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        resp = {"status": "success"}

    except SQLAlchemyError:
        current_app.logger.error("DB error: Unique user and experiment combination not found.")
        resp = {"status": "error, uniqueId and/or experiment not found"}

    return jsonify(**resp)


@experiments.route('/sync/<id_exp>', methods=['GET'])
def load(id_exp=None):
    """
    Load experiment data, which should be a JSON object and will be stored
    after converting to string.
    """
    current_app.logger.info("GET /sync route with id: %s" % id_exp)

    try:
        unique_id, experiment_name = id_exp.split("&")
        user = Participant.query.\
            filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).\
            one()
    except SQLAlchemyError:
        current_app.logger.error("DB error: Unique user /experimetn combo not found.")

    try:
        resp = json.loads(user.datastring)
    except:
        resp = {
            "uniqueId": user.uniqueid,
            "experimentName" : user.experimentname
        }

    return jsonify(**resp)

@experiments.route('/sync/<id_exp>', methods=['PUT'])
def update(id_exp=None):
    """
    Save experiment data, which should be a JSON object and will be stored
    after converting to string.
    """
    current_app.logger.info("PUT /sync route with id: %s" % id_exp)

    try:
        unique_id, experiment_name = id_exp.split("&")
        user = Participant.query.\
            filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).\
            one()
    except SQLAlchemyError:
        current_app.logger.error("DB error: Unique user not found.")

    if hasattr(request, 'json'):
        user.datastring = request.get_data().decode('utf-8').encode(
            'ascii', 'xmlcharrefreplace'
        )
        db.session.add(user)
        db.session.commit()

    try:
        data = json.loads(user.datastring)
    except:
        data = {}

    trial = data.get("currenttrial", None)
    current_app.logger.info("saved data for %s, experiment %s (current trial: %s)", unique_id, experiment_name, trial)
    resp = {"status": "user data saved"}
    return jsonify(**resp)

@experiments.route('/quitter', methods=['POST'])
def quitter():
    """ Mark quitter as such. """
    if not ('uniqueId' in request.form) or not ('experimentName' in request.form):
        resp = {"status": "bad request"}
        return jsonify(**resp)

    unique_id = request.form['uniqueId']
    experiment_name = request.form['experimentName']

    if unique_id[:5] == "debug":
        debug_mode = True
    else:
        debug_mode = False

    if debug_mode:
        resp = {"status": "didn't mark as quitter since this is debugging"}
        return jsonify(**resp)
    else:
        try:
            current_app.logger.info("Marking quitter %s in experiment %s" % (unique_id, experiment_name))
            user = Participant.query.\
                filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).\
                one()
            user.status = 6
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            raise ExperimentError('tried_to_quit')
        else:
            resp = {"status": "marked as quitter"}
            return jsonify(**resp)

@experiments.route('/worker_complete', methods=['GET'])
def worker_complete():
    """Complete worker."""

    if not ('uniqueId' in request.args) or not ('experimentName' in request.args):
        raise ExperimentError('improper_inputs')
                
    else:
        unique_id = request.args['uniqueId']
        experiment_name = request.args['experimentName']

        current_app.logger.info("Completed experiment %s, %s" % (unique_id, experiment_name))
        try:
            user = Participant.query.\
                filter((Participant.uniqueid == unique_id) & (Participant.experimentname == experiment_name)).\
                one()
            user.status = 3
            user.endhit = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError:
           raise ExperimentError('unknown_error')

        return render_template("complete.html")

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
        return render_template("error.html", errornum = 404)


@experiments.errorhandler(ExperimentError)
def handle_exp_error(exception):
    """Handle errors by sending an error page."""
    current_app.logger.error(
        "%s (%s) %s", exception.value, exception.errornum, str(dict(request.args)))
    return exception.error_page(request, "delavega@colorado.edu")

