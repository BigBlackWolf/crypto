from flask_migrate import MigrateCommand
from flask_script import Manager
import logging

from app import create_app


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.DEBUG)

    app = create_app()
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
