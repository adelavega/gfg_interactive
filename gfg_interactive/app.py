# -*- coding: utf-8 -*-
""" This module provides the backend Flask server. """
# Setup flask
from flask import Flask, render_template
from experiments import experiments
#from dashboard import dashboard
import os
from database import db
import ConfigParser

print os.path.join(os.path.dirname(__file__), "config.ini")
# Load configuration
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

app = Flask(__name__)
app.config.from_object(Config.get("General", "config"))
app.register_blueprint(experiments, url_prefix='/exp')

db.init_app(app)


@app.route('/')
def index():
    ''' Index route '''
    return render_template('default.html')


@app.route('/favicon.ico')
def favicon():
    ''' Serve favicon '''
    return app.send_static_file('favicon.ico')
if __name__ == '__main__':
	app.debug = True
	app.run()
