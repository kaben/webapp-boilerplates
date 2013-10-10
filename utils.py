from flask import flash, redirect, session, url_for
from functools import wraps

# Convenience functions.
def flash_errors(form):
  for field, errors in form.errors.items():
    for error in errors:
      flash("Error in the '{}' field: {}".format(getattr(form, field).label.text, error), "error")

def login_required(f):
  @wraps(f)
  def wrap(*args, **kw):
    if "logged_in" in session:
      return f(*args, **kw)
    else:
      flash("Please login.")
      return redirect(url_for("login"))
  return wrap


