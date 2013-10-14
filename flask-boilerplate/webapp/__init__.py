# Configure logging before importing anything that also configures logging.
from config import logging_config_dict
import logging.config
logging.config.dictConfig(logging_config_dict)
log = logging.getLogger()
log.debug("logging enabled!")

# Remaining imports.
from forms import LoginForm
from models import ORM
from utils import flash_errors, login_required
from flask import Flask, flash, redirect, render_template, request, session, url_for
 
# Setup Flask app.
app = Flask(__name__)
app.config.from_object("config")
# Also setup app to use SQLAlchemy models.
orm = ORM(app)
db = orm.db
app.config["orm"] = orm
app.config["db"] = db

from hello_world.views import mod as hello_world_mod
from register.views import mod as register_mod
app.register_blueprint(hello_world_mod)
app.register_blueprint(register_mod)

@app.route("/login", methods=["GET", "POST"])
def login():
  error = None
  if request.method == "POST":
    login = request.form["user"]
    password = request.form["password"]
    user = orm.User.query.filter_by(login=login, password=password).first()
    if user is None:
      error = "Invalid user/password."
    else:
      session["logged_in"] = True
      flash("Logged in.")
      return redirect(url_for("home"))
  form = LoginForm(request.form)
  return render_template("login.html", form=form, error=error)

@app.route("/logout")
def logout():
  session.pop("logged_in", None)
  flash("Logged out.")
  return redirect(url_for("login"))

@app.route("/")
@app.route("/home")
@login_required
def home():
  return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

