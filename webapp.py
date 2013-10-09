#!/usr/bin/env python

# Configure logging before importing anything that also configures logging.
import logging.config
logging_config_dict = {
  "version": 1,
  "formatters": {"simple": {"format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"}},
  "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
  "root": {"level": "DEBUG", "propagate": True, "handlers": ["console"]},
  "disable_existing_loggers": False,
}
logging.config.dictConfig(logging_config_dict)
log = logging.getLogger()
log.debug("logging enabled!")

# Remaining imports.
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from flask.ext.wtf import PasswordField, TextField
from flask.ext.wtf import EqualTo, Length, Required
 
# Flask configuration searches given module for UPPERCASE objects...
SQLALCHEMY_DATABASE_URI = "sqlite:///hello.db"
SECRET_KEY = "\xd8\x1e\x88\xf4\xb7\xa9@\xb8p\n2v\x1d\xb5\xb9IfA\xf6\x14\x80\x89\xf4F"

# Setup Flask app.
app = Flask(__name__)
app.config.from_object(__name__)
# Also setup app to use SQLAlchemy.
db = SQLAlchemy(app)

# Database models.
class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  login = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return "<User login: '{login}', email: '{email}'>".format(**self.__dict__)

# HTML forms.
class LoginForm(Form):
  user = TextField("User", validators=[Required()])
  password = PasswordField("Password", validators=[Required()])

class RegisterForm(Form):
  user = TextField("User", validators=[Required(), Length(min=5, max=25)])
  email = TextField("Email", validators=[Required(), Length(min=5, max=40)])
  password = PasswordField("Password", validators=[Required(), Length(min=10, max=40)])
  confirm = PasswordField("Confirm password", validators=[EqualTo("password", message="Passwords must match")])

# Convenience functions.
def flash_errors(form):
  for field, errors in form.errors.items():
    for error in errors:
      flash("Error in the '{}' field: {}".format(getattr(form, field).label.text, error), "error")

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
      return redirect(url_for("hello"))
  form = LoginForm(request.form)
  return render_template("login.html", form=form, error=error)

@app.route("/logout")
def logout():
  session.pop("logged_in", None)
  flash("Logged out.")
  return redirect(url_for("login"))

@app.route("/hello")
def hello():
  return render_template("hello.html", title="Hi there.")

# If this script is being executed instead of imported, run the webapp.
if __name__ == "__main__": app.run()

