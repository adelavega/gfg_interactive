from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import ConfigParser 
from app import app, db
import os

# Load configuration
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
app.config.from_object(Config.get("General", "config"))


migrate = Migrate(app, db, compare=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
