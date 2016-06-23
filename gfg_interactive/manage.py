from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import ConfigParser 
from app import app, db

# Load configuration
Config = ConfigParser.ConfigParser()
Config.read("../config.ini")
app.config.from_object(Config.get("General", "config"))


migrate = Migrate(app, db, compare=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
