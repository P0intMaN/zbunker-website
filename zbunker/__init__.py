from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_mail import Mail
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS"))

db = SQLAlchemy(app)
if db.engine.url.drivername == 'sqlite':
    migrate = Migrate(app, db, render_as_batch=True)
else:
    migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from zbunker import routes, models
