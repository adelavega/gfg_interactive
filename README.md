# GfG Interactive Survey Module
This module serves interactive javascript surveys (such as cognitive tasks) for GenesforGood. This module was original 
based on psiTurk, and uses an identical javascript API to send data back to the server (here called dataHandler). 

## Installation
Basic dependencies:

* Flask
* Flask-Migrate
* Flask-SQLAlchemy
* Alembic
* mysql-python

To install dependencies run the following command. It is reccomended you do this in a virtual environment (set up 
virtualenv one folder above this one). Make sure to also install the correct dependency for your DB manually.

`pip -r requirements.txt`

## Configuration
The type of configuration is set using the config.ini file. By default, it is set to "HomeConfig" which is for local 
testing. Edit this file to match the appropriate configuration (e.g. Staging, Production).

The file wsgi/config.py specifies configuration details, such as the database URI and credentials to use. 
COPY example_config.py to config.py and edit with the appropriate details. Ensure that you have already created the 
specific database(s) to be used. 

## Database set up and initial migration
We use Alembic to track database migrations. To initiate the db and perform the first migration, activate your virtual 
environment, then run the following commands.

(**You may be able to omit the first two db commands**, in which case error messages during those steps may be ignored) 

```bash
$ cd gfg_interactive
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade 
```

## Deployment and testing
### Devbox deployment
1) Clone this repo into an appropriate location and symlink to `/srv/www/genesforgood/current/gfg-interactive` 
(or other directory as appropriate)

2) Install pip:
```bash
$ curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
$ sudo python get-pip.py
``` 
3) Install system dependencies

`sudo apt-get install python-dev libmysqlclient-dev libapache2-mod-wsgi`
    
4) Create virtual environment and activate (in `/srv/www/genesforgood/current/gfg-interactive/`)

```bash
$ virtualenv venv
$ source venv/bin/activate.csh
```
    
5) Install python dependencies

`pip install -r requirements.txt`
    
6) Copy config files from example ones and add SQL credentials. Make sure `config.ini` is in `gfg-interactive/` 
and points to a complete config block defined in gfg-interactive/config.py (see gfg-interactive/example.config.py 
for a template). Make sure to define credentials for the research database, the SQL Alchemy URL for the interactive 
database (which includes all DB creds on one line) **and that the secret key matches the MODULE_INTEGRATION_KEY value 
for the genes for good PHP app configuration**.

7) Set permission of relevant files to +755 

`sudo chmod -R +755 gfg-interactive/`

8) Edit apache config to enable WSGI. Relevant section should look like:

```
WSGIDaemonProcess gfg-interactive user=www-data group=www-data threads=5
WSGIScriptAlias /gfg-interactive /srv/www/genesforgood/etc/gfg_interactive.wsgi
<Directory "/srv/www/genesforgood/current/gfg-interactive">
    WSGIProcessGroup gfg-interactive
    WSGIApplicationGroup %{GLOBAL}
    Require all granted
</Directory>
```

If you are using a virtual environment, be sure to edit `gfginteractive.wsgi` to point at the correct 
virtualenv script location and code directory. The Apache directive should also be edited to point to the correct 
folders where your code is housed.

9) Follow the instructions above to initialize your DB.

**Tip**: On some servers, the configuration in step 8 will only take effect if `GFG_SSL` has been defined in the 
default HTTPS virtualhost file (eg `001-default-ssl.conf` or similar). 

If interactive surveys fail with a 404 error, check server configuration. 

## Documentation
The flask project has the following files/sections:

 * The basic app.py file. In this app this doesn't do much except link the rest of the following parts together
 * experiments.py - This file handles all routes to /exp and serves the individual experiments. **This is the most 
 important section for actually serving experiments and collecting data**.
 * errors.py - This file contains an error handler that routes to an appropriate error page when things go wrong
 * models.py - This file defines the data models. 
 * manage.py - This file contains the logic for updating your database. See deployment for more info. Make sure to run 
 the relevant commands when models.py is updated.

### Experiments
The experiments.py file serves the experiments set up in the app. Without editing more than a line of code, it is 
possible to add a new task to the server. In experiments.py, the experiment_list variable defines the experiments 
associated to a unique surveyid. Each experiment is a tuple of (surveyid, experiment_name). 

Each experiment has its own folders under both /exp/static and /exp/templates. For example, the task "keep_track" has 
its javascript files under:
`/exp/static/keep_track/js/`
and its main html template under
`/exp/static/keep_track/exp.html`

### Experiment setup and dataHandler.js API
This is how you set up your javascript experiment to work with this server. 

The only real requirement is that an exp.html file exists under the right folder and that that file defines the 
following variable in javascript:

```html
<script type="text/javascript">
	var uniqueid = "{{ uniqueid }}";
	var sessionid = "{{ sessionid }}";
	var experimentname = "{{ experimentname }}";
	var surveyid = "{{ surveyid }}";
	var debug = "{{ debug }}";
</script>
```

and imports important libraries such as jQuery,  this app's dataHandler.js, and it's own js files, of course:

```html
<script src="static/js/dataHandler.js"></script>
<script src="static/{{ experimentName }}/js/task.js"></script>
<script src="static/lib/jquery-min.js" type="text/javascript"> </script>
```

You can then do the following things with the dataHandler object:

* Load preloaded page

	`return $('body').html(dataHandler.getPage('postquestionnaire.html'));`
* Save trial data (an array)

	`dataHandler.recordTrialData(['500ms', 'trial1'])`
- Record unstructured data (e.g. questionnaire info)

	`dataHandler.recordUnstructuredData('openended', $('#openended').val());`
* Save data to server (do this somewhat often and before quitting)

	`dataHandler.saveData();`
* Complete the task and get set back to landing page (edit this for the message you want to send after the task is 
done or edit the code to close window or navigate elsewhere)

	`dataHandler.completeHIT();`
	
Aside from that, its up to you to build whatever javascript assessment you want and this server should record the data 
and serve it appropriately. 
