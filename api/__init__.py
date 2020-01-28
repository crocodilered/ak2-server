from db import Db
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
import psycopg2


app = Flask('ak2')

app_config = os.getenv('AK2_CONFIG', 'api.config.DevelopmentConfig')
app.config.from_object(app_config)

# Wake up CORS
CORS(app)

# Wake up bcrypt
bcrypt = Bcrypt(app)


# TODO: think to move this somewhere.
# Wake up database
db = Db(psycopg2.connect(app.config.get('DATABASE_URI')), app.config.get('DATABASE_SCHEMA'))


# Register blueprints
from api.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from api.users.views import users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/users')

from api.sections.views import sections_blueprint
app.register_blueprint(sections_blueprint, url_prefix='/sections')
