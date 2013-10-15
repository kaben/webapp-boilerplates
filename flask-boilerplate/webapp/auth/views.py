from forms import LoginForm
from ..utils import flash_errors
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for


mod = Blueprint(
  "auth",
  __name__,
  url_prefix="/auth",
  template_folder="templates",
  static_folder="static",
)

@mod.route("/", methods=["GET", "POST"])
def login():
  error = None
  if request.method == "POST":
    login = request.form["user"]
    password = request.form["password"]
    orm = current_app.config["orm"]
    user = orm.User.query.filter_by(login=login, password=password).first()
    if user is None:
      error = "Invalid user/password."
    else:
      session["logged_in"] = True
      flash("Logged in.")
      return redirect(url_for("home"))
  form = LoginForm(request.form)
  return render_template("login.html", form=form, error=error)

@mod.route("/logout")
def logout():
  session.pop("logged_in", None)
  flash("Logged out.")
  return redirect(url_for("auth.login"))

