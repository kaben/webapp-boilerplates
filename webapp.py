#!/usr/bin/env python

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
 
SQLALCHEMY_DATABASE_URI = "sqlite:///hello.db"
  
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  login = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)

@app.route("/hello")
def hello():
  return render_template("hello.html", title="Hi there.")

if __name__ == "__main__": app.run()

