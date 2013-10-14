# Configure logging before importing anything that also configures logging.
from config import logging_config_dict
import logging.config
logging.config.dictConfig(logging_config_dict)
log = logging.getLogger()
log.debug("logging enabled!")

# Remaining imports.
from forms import LoginForm, RegisterForm
from models import ORM
from utils import flash_errors, login_required
from flask import Flask, flash, redirect, render_template, request, session, url_for
 
# Setup Flask app.
app = Flask(__name__)
app.config.from_object("config")
# Also setup app to use SQLAlchemy models.
orm = ORM(app)
db = orm.db
User = orm.User

from hello_world.views import mod as hello_world_mod
app.register_blueprint(hello_world_mod)

# Web interface controllers.
@app.route("/register", methods=["GET", "POST"])
def register():
  error = None
  form = RegisterForm(request.form, csrf_enabled=False)
  if form.validate_on_submit():
    new_user = User(
      login=form.user.data,
      email=form.email.data,
      password=form.password.data,
    )
    db.session.add(new_user)
    db.session.commit()
    flash("Registered! Please login.")
    return redirect(url_for('login'))
  else: flash_errors(form)
  return render_template("register.html", form=form, error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
  error = None
  if request.method == "POST":
    login = request.form["user"]
    password = request.form["password"]
    user = User.query.filter_by(login=login, password=password).first()
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

#@app.route("/hello")
#def hello():
#  return render_template("hello.html")

