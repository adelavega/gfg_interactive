activate_this = '/srv/www/genesforgood/current/gfg-interactive/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/srv/www/genesforgood/current/gfg-interactive/gfg_interactive")

from app import app as application
