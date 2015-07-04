# -*- coding: utf-8 -*-
""" This module provides the backend Flask server. """
import os

# Setup flask
from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from utils import nocache
from errors import ExperimentError
import json

import datetime

# Status codes
NOT_ACCEPTED = 0
ALLOCATED = 1
STARTED = 2
COMPLETED = 3
QUITEARLY = 6



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

from database import db
db.init_app(app)

from models import Participant

@app.route('/')
@nocache
def index():
    ''' Index route '''
    return render_template('default.html')

@app.route('/exp', methods=['GET'])
@nocache
def start_exp():
    """ Serves up the experiment applet. """

    if not ('uniqueId' in request.args):
        raise ExperimentError('hit_assign_worker_id_not_set_in_exp')

    unique_id = request.args['uniqueId']

    app.logger.info("Accessing /exp: %(i)s" % {
        "i" : unique_id})

    # Check first to see if this hitId or assignmentId exists.  If so, check to
    # see if inExp is set
    matches = Participant.query.\
        filter(Participant.uniqueid == unique_id).\
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

        part = Participant(uniqueid=unique_id, ipaddress=worker_ip, browser=browser, platform=platform, language=language)

        db.session.add(part)
        db.session.commit()

    elif numrecs == 1:
        # They've already done an assignment, then we should tell them they
        #    can't do another one

        part = matches[0]

        ## Status
        if part.status == 2:
        	raise ExperimentError('already_started_exp')

        
    return render_template('exp.html', uniqueId=part.uniqueid)


@app.route('/inexp', methods=['POST'])
def enterexp():
    """
    AJAX listener that listens for a signal from the user's script when they
    leave the instructions and enter the real experiment. After the server
    receives this signal, it will no longer allow them to re-access the
    experiment applet (meaning they can't do part of the experiment and
    referesh to start over).
    """
    app.logger.info("Accessing /inexp")
    if not 'uniqueId' in request.form:
        raise ExperimentError('improper_inputs')
    unique_id = request.form['uniqueId']

    try:
        user = Participant.query.\
            filter(Participant.uniqueid == unique_id).one()
        user.status = 2
        user.beginexp = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        resp = {"status": "success"}
    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.error("DB error: Unique user not found.")
        resp = {"status": "error, uniqueId not found"}
    return jsonify(**resp)


@app.route('/sync/<uid>', methods=['GET'])
def load(uid=None):
    """
    Load experiment data, which should be a JSON object and will be stored
    after converting to string.
    """
    app.logger.info("GET /sync route with id: %s" % uid)

    try:
        user = Participant.query.\
            filter(Participant.uniqueid == uid).\
            one()
    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.error("DB error: Unique user not found.")

    try:
        resp = json.loads(user.datastring)
    except:
        resp = {
            "condition": user.cond,
            "counterbalance": user.counterbalance,
            "assignmentId": user.assignmentid,
            "workerId": user.workerid,
            "hitId": user.hitid,
            "bonus": user.bonus
        }

    return jsonify(**resp)

@app.route('/sync/<uid>', methods=['PUT'])
def update(uid=None):
    """
    Save experiment data, which should be a JSON object and will be stored
    after converting to string.
    """
    app.logger.info("PUT /sync route with id: %s" % uid)

    try:
        user = Participant.query.\
            filter(Participant.uniqueid == uid).\
            one()
    except SQLAlchemy.exc.SQLAlchemyError:
        app.logger.error("DB error: Unique user not found.")

    if hasattr(request, 'json'):
        user.datastring = request.data.decode('utf-8').encode(
            'ascii', 'xmlcharrefreplace'
        )
        db.session.add(user)
        db.session.commit()

    try:
        data = json.loads(user.datastring)
    except:
        data = {}

    trial = data.get("currenttrial", None)
    app.logger.info("saved data for %s (current trial: %s)", uid, trial)
    resp = {"status": "user data saved"}
    return jsonify(**resp)

@app.route('/quitter', methods=['POST'])
def quitter():
    """
    Mark quitter as such.
    """
    unique_id = request.form['uniqueId']
    if unique_id[:5] == "debug":
        debug_mode = True
    else:
        debug_mode = False

    if debug_mode:
        resp = {"status": "didn't mark as quitter since this is debugging"}
        return jsonify(**resp)
    else:
        try:
            unique_id = request.form['uniqueId']
            app.logger.info("Marking quitter %s" % unique_id)
            user = Participant.query.\
                filter(Participant.uniqueid == unique_id).\
                one()
            user.status = 6
            db.session.add(user)
            db.session.commit()
        except SQLAlchemy.exc.SQLAlchemyError:
            raise ExperimentError('tried_to_quit')
        else:
            resp = {"status": "marked as quitter"}
            return jsonify(**resp)

@app.route('/worker_complete', methods=['GET'])
def worker_complete():
    ''' Complete worker. '''
    if not 'uniqueId' in request.args:
        resp = {"status": "bad request"}
        return jsonify(**resp)
    else:
        unique_id = request.args['uniqueId']
        app.logger.info("Completed experiment %s" % unique_id)
        try:
            user = Participant.query.\
                filter(Participant.uniqueid == unique_id).one()
            user.status = "completed"
            user.endhit = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            status = "success"
        except SQLAlchemy.exc.SQLAlchemyError:
            status = "database error"
        resp = {"status" : status}
        return jsonify(**resp)


@app.errorhandler(ExperimentError)
def handle_exp_error(exception):
    """Handle errors by sending an error page."""
    app.logger.error(
        "%s (%s) %s", exception.value, exception.errornum, str(dict(request.args)))
    return exception.error_page(request, "delavega@colorado.edu")

@app.route('/favicon.ico')
def favicon():
    ''' Serve favicon '''
    return app.send_static_file('/static/favicon.ico')

# Generic route
@app.route('/<pagename>')
@app.route('/<foldername>/<pagename>')
def regularpage(foldername=None, pagename=None):
    """
    Route not found by the other routes above. May point to a static template.
    """
    if foldername is None and pagename is None:
        raise ExperimentError('page_not_found')
    if foldername is None and pagename is not None:
        return render_template(pagename)
    else:
        return render_template(foldername+"/"+pagename)

if __name__ == '__main__':
	app.debug = True
	app.run()