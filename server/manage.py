import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from main import create_flask_app


environment = os.getenv("FLASK_CONFIG")
app = create_flask_app(environment)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
