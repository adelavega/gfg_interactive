# -*- coding: utf-8 -*-
""" This module provides the backend Flask server. """
import os

# Setup flask
from flask import Flask, render_template
from utils import nocache

from experiments import experiments
from dashboard import dashboard

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.register_blueprint(experiments, url_prefix='/exp')
app.register_blueprint(dashboard, url_prefix='/dashboard')

from database import db
db.init_app(app)


@app.route('/')
@nocache
def index():
    ''' Index route '''
    return render_template('default.html')


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
    from jinja2.exceptions import TemplateNotFound

    try: 
        
	    if foldername is None and pagename is not None:
	        return render_template(pagename)
	    else:
    		return render_template(foldername+"/"+pagename)
    except TemplateNotFound:
    	return render_template("error.html", errornum = 404)

if __name__ == '__main__':
	app.debug = True
	app.run()