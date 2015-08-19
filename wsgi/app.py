# -*- coding: utf-8 -*-
""" This module provides the backend Flask server. """
import os

# Setup flask
from flask import Flask, render_template
from experiments import experiments
from dashboard import dashboard

from database import db

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.register_blueprint(experiments, url_prefix='/exp')
app.register_blueprint(dashboard, url_prefix='/dashboard')

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