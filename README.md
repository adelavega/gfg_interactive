# GfG Interactive Survey Module
This module serves interactive javascript surveys (such as cognitive tasks) for GenesforGood. This module was original based on psiTurk, and uses an identical javascript API to send data back to the server (here called dataHandler). 

## Installation
Basic dependencies:

* Flask
* Flask-Migrate
* Flask-SQLAlchemy
* Alembic

If using Postgres:
* Psycopg2

If using MySQL:
* mysql-python

To install dependencies run the following command. It is reccomended you do this in a virtual environment (set up virtualenv one folder above this one). Make sure to also install the correct dependency for your DB manually.

    pip -r requirements.txt

### Configuration
The type of configuration is set using the config.ini file. By default, it is set to "HomeConfig" which is for local testing. Edit this file to match the appropriate configuration (e.g. Staging, Production).

The file wsgi/config.py specifies configuration details, such as the database URI and credentials to use. 
COPY example_config.py to config.py and edit with the appropriate details. Ensure that you have credted a specific database to be used. 

### Database set up and inital migration
We use Alembic to track database migrations. To initate the db and perform the first migration, run the following commands:

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    
    
## Deployment and testing
### Devbox deployment
1) Clone this repo into /var/www

2) Install pip:

    curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
    sudo python get-pip.py
    
3) Install system dependencies

    sudo apt-get install python-dev libmysqlclient-dev libapache2-mod-wsgi
    
4) Create virtual environment and activate (in /var/www/gfginteractive)

    virtualenv venv
    source venv/bin/activate
    
5) Install python dependencies

    pip install -r requirements.txt
    
6) Copy config files from example ones and add SQL credentials. Also, make sure config.ini is in gfg_interactive/

7) Set permission of relevant files to +755 

    sudo chmod -R +755 gfg-interactive/

8) Edit apache config to enable WSGI. Relevant section should look like:

    WSGIDaemonProcess gfg-interactive user=www-data group=www-data threads=5
    WSGIScriptAlias /gfg-interactive /var/www/gfginteractive/gfginteractive.wsgi
    <Directory "/var/www/gfginteractive/">
        WSGIProcessGroup gfg-interactive
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>

9) Initatialize db

    sudo gfginteractive/venv/bin/python gfginteractive/gfg_interactive/manage.py db init
    sudo gfginteractive/venv/bin/python gfginteractive/gfg_interactive/manage.py db migrate
    sudo gfginteractive/venv/bin/python gfginteractive/gfg_interactive/manage.py db upgrade

	
## Documentation
The flask project has the following files/sections:

 * The basic app.py file. In this app this doesn't do much except link the rest of the following parts together
 * experiments.py - This file handles all routes to /exp and serves the individual experiments. **This is the most important section for actually serving experiments and collecting data**.
 * errors.py - This file contains an error handler that routes to an appropriate error page when things go wrong
 * models.py - This file defines the data models. 
 * manage.py - This file contains the logic for updating your database. See deployment for more info. Ensure to run the relevant commands when models.py is updated.

### Experiments
The experiments.py file serves the experiments set up in the app. Without editing more than a line of code, it is possible to add a new task to the server. In experiments.py, the experiment_list variable defines the experiments associated to a unique surveyid. Each experiment is a tuple of (surveyid, experiment_name). 

Each experiment has its own folders under both /exp/static and /exp/templates. For example, the task "keep_track" has its javascript files under:
/exp/static/keep_track/js/
and its main html template under
/exp/static/keep_track/exp.html

### Experiment setup and dataHandler.js API
This is how you set up your javascript experiment to work with this server. 

The only real requirement is that an exp.html file exists under the right folder and that that file defines the following variable in javascript:

	<script type="text/javascript">
		var uniqueid = "{{ uniqueid }}";
		var sessionid = "{{ sessionid }}"
		var experimentname = "{{ experimentname }}"
		var surveyid = "{{ surveyid }}"
		var debug = "{{ debug }}"
	</script>

and imports important libraries such as jQuery,  this app's dataHandler.js, and it's own js files, of course:

	<script src="static/js/dataHandler.js"></script>
	<script src="static/{{ experimentName }}/js/task.js"></script>
	<script src="static/lib/jquery-min.js" type="text/javascript"> </script>

You can then do the following things with the dataHandler object:

* Load preloaded page

	return $('body').html(dataHandler.getPage('postquestionnaire.html'));
* Save trial data (an array)

	dataHandler.recordTrialData(['500ms', 'trial1'])
- Record unstructured data (e.g. questionnaire info)

	dataHandler.recordUnstructuredData('openended', $('#openended').val());
* Save data to server (do this somewhat often and before quitting)

	dataHandler.saveData();
* Complete the task and get set back to landing page (edit this for the message you want to send after the task is done or edit the code to close window or navigate elsewhere)

	dataHandler.completeHIT();
	
Aside from that, its up to you to build whatever javascript assesment you want and this server should record the data and serve it appropriately. 
