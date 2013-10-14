from forms import RegisterForm
from ..utils import flash_errors
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for


mod = Blueprint(
  "register",
  __name__,
  url_prefix="/register",
  template_folder="templates",
  static_folder="static",
)

@mod.route("/", methods=["GET", "POST"])
def register():
  error = None
  form = RegisterForm(request.form, csrf_enabled=False)
  if form.validate_on_submit():
    orm = current_app.config["orm"]
    new_user = orm.User(
      login=form.user.data,
      email=form.email.data,
      password=form.password.data,
    )
    orm.db.session.add(new_user)
    orm.db.session.commit()
    flash("Registered! Please login.")
    return redirect(url_for('login'))
  else: flash_errors(form)
  return render_template("register.html", form=form, error=error)

