#!/usr/bin/env python

import webapp
from flask import flash, render_template, session
import unittest

def setup_database():
  webapp.app.config["TESTING"] = True
  # Tell SQLAlchemy to use an in-memory database.
  webapp.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
  webapp.db.create_all()

class TestHello(unittest.TestCase):
  def setUp(self):
    setup_database()
    self.client = webapp.app.test_client()

  def tearDown(self):
    webapp.db.drop_all()

  def test_hello(self):
    self.assertTrue("Hello" in self.client.get("/hello").data)

  def test_db_setup(self):
    user = webapp.User(login="foo", email="foo@gmail.com", password="password")
    webapp.db.session.add(user)
    webapp.db.session.commit()

  def test_populate_db_script(self):
    # The populate_db script should create some users.
    import populate_db
    populate_db.populate_database(webapp)
    query = webapp.db.session.query(webapp.User)
    self.assertTrue(0 < query.count())
    
  def test_view_db_script(self):
    # The view_db script should return a string with info about all users.
    import view_db
    webapp.db.session.add(webapp.User(login="foo", email="foo@gmail.com", password="password"))
    webapp.db.session.add(webapp.User(login="bar", email="bar@gmail.com", password="password"))
    webapp.db.session.commit()
    dump = view_db.view_database(webapp)
    self.assertTrue("foo" in dump)
    self.assertTrue("bar" in dump)

  def test_flashed_messages(self):
    @webapp.app.route("/flashtest")
    def flashtest():
      flash("Testing flashed messages.")
      return render_template("hello.html", title="Hi there.")
    self.assertTrue("Testing flashed messages." in self.client.get("/flashtest").data)
    
  def test_error_messages(self):
    @webapp.app.route("/errortest")
    def errortest():
      error = "This is an error!"
      return render_template("hello.html", title="Hi there.", error=error)
    self.assertTrue("This is an error!" in self.client.get("/errortest").data)

class TestLogin(unittest.TestCase):
  def setUp(self):
    setup_database()
    self.client = webapp.app.test_client()
    user = webapp.User(login="foo", email="foo@gmail.com", password="password")
    webapp.db.session.add(user)
    webapp.db.session.commit()

  def tearDown(self):
    webapp.db.drop_all()

  def test_login_get(self):
    data = self.client.get("/login").data
    self.assertTrue("User" in data)
    self.assertTrue("Password" in data)

  def test_valid_login_put(self):
    data = self.client.post("/login", data=dict(user="foo", password="password")).data
    with self.client.session_transaction() as session:
      self.assertTrue(session["logged_in"])
    self.assertTrue("Logged in" in data)

  def test_valid_login_put(self):
    data = self.client.post("/login", data=dict(user="invalid", password="invalid")).data
    with self.client.session_transaction() as session:
      self.assertTrue(not "logged_in" in session)
    self.assertTrue("Invalid user" in data)

if __name__ == "__main__": unittest.main()

