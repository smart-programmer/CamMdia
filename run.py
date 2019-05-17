from WEBSITE import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys

migrate = Migrate(app, db)

manager = Manager(app)
command = "db"
manager.add_command(command, MigrateCommand)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == command:
            manager.run()
    else:
        app.run(debug=True)
