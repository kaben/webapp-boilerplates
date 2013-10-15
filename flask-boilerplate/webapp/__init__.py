# Configure logging before importing anything that also configures logging.
from config import logging_config_dict
import logging.config
logging.config.dictConfig(logging_config_dict)
log = logging.getLogger()
log.debug("logging enabled!")

# Remaining imports.
from models import ORM
from utils import login_required
from flask import Flask, render_template
 
# Setup Flask app.
app = Flask(__name__)
app.config.from_object("config")
# Also setup app to use SQLAlchemy models.
orm = ORM(app)
app.config["orm"] = orm

from hello_world.views import mod as hello_world_mod
from auth.views import mod as auth_mod
from register.views import mod as register_mod
app.register_blueprint(hello_world_mod)
app.register_blueprint(auth_mod)
app.register_blueprint(register_mod)

@app.route("/")
@app.route("/home")
@login_required
def home():
  return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

