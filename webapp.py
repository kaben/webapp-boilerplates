#!/usr/bin/env python

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, Required
from flask.ext.wtf import PasswordField, TextField
 
SQLALCHEMY_DATABASE_URI = "sqlite:///hello.db"
SECRET_KEY = "\xd8\x1e\x88\xf4\xb7\xa9@\xb8p\n2v\x1d\xb5\xb9IfA\xf6\x14\x80\x89\xf4F"
  
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  login = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

  def __repr__(self):
    return "<User login: '{login}', email: '{email}'>".format(**self.__dict__)

class LoginForm(Form):
  user = TextField("User", validators=[Required()])
  password = PasswordField("Password", validators=[Required()])

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

@app.route("/hello")
def hello():
  return render_template("hello.html", title="Hi there.")

if __name__ == "__main__": app.run()

