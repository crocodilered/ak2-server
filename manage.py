from flask_script import Manager
from api import app


if __name__ == '__main__':
    manager = Manager(app)
    manager.run()
