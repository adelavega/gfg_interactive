activate_this = '/var/www/gfginteractive/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/gfginteractive/gfg_interactive")

from app import app as application
