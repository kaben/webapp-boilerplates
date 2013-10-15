#!/usr/bin/env python

import webapp
from flask import flash, render_template, request, session
import unittest

def setup_database():
  webapp.app.config["TESTING"] = True
  # Tell SQLAlchemy to use an in-memory database.
  webapp.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
  webapp.orm.db.create_all()


class TestHello(unittest.TestCase):
  def setUp(self):
    self.client = webapp.app.test_client()

  def test_hello_world(self):
    # Verifies client-server interaction with simple hello-world.
    data = self.client.get("/hello_world/").data
    self.assertTrue("Hello" in data)


class TestWebapp(unittest.TestCase):
  def setUp(self):
    setup_database()
    self.client = webapp.app.test_client()

  def tearDown(self):
    webapp.orm.db.drop_all()

  def test_about(self):
    self.assertTrue("About" in self.client.get("/about").data)

  def test_home(self):
    # Verifies client-server interaction with simple hello-world.
    with self.client.session_transaction() as session:
      session["logged_in"] = True
    self.assertTrue("Home" in self.client.get("/home").data)

  def test_db_setup(self):
    # Verifies database functions well enough for committing data.
    user = webapp.orm.User(login="foo", email="foo@gmail.com", password="password")
    webapp.orm.db.session.add(user)
    webapp.orm.db.session.commit()

  def test_populate_db_script(self):
    # The populate_db script should create some users.
    import populate_db
    populate_db.populate_database(webapp)
    query = webapp.orm.db.session.query(webapp.orm.User)
    self.assertTrue(0 < query.count())
    
  def test_view_db_script(self):
    # The view_db script should return a string with info about all users.
    import view_db
    webapp.orm.db.session.add(webapp.orm.User(login="foo", email="foo@gmail.com", password="password"))
    webapp.orm.db.session.add(webapp.orm.User(login="bar", email="bar@gmail.com", password="password"))
    webapp.orm.db.session.commit()
    dump = view_db.view_database(webapp)
    self.assertTrue("foo" in dump)
    self.assertTrue("bar" in dump)

  def test_flashed_messages(self):
    # Verifies that "main_layout.html" template processes flashed messages.
    # I don't like that "about.html" is hardwired into this test.
    @webapp.app.route("/flash_test")
    def flash_test():
      flash("Testing flashed messages.")
      return render_template("about.html")
    self.assertTrue("Testing flashed messages." in self.client.get("/flash_test").data)
    
  def test_error_messages(self):
    # Verifies that "main_layout.html" template processes error messages.
    # I don't like that "about.html" is hardwired into this test.
    @webapp.app.route("/error_test")
    def error_test():
      error = "This is an error!"
      return render_template("about.html", error=error)
    self.assertTrue("This is an error!" in self.client.get("/error_test").data)

  def test_flash_form_errors(self):
    @webapp.app.route("/flash_form_error_test", methods=["POST"])
    def flash_form_error_test():
      form = webapp.auth.forms.LoginForm(request.form)
      if not form.validate_on_submit():
        webapp.utils.flash_errors(form)
      return render_template("about.html")
    post_data = dict(user="", password="")
    data = self.client.post("/flash_form_error_test", data=post_data).data
    self.assertTrue("field is required" in data)


class TestRegistration(unittest.TestCase):
  def setUp(self):
    setup_database()
    self.client = webapp.app.test_client()
    # Add a user to the database.
    user = webapp.orm.User(login="foo", email="foo@gmail.com", password="password")
    webapp.orm.db.session.add(user)
    webapp.orm.db.session.commit()

  def tearDown(self):
    webapp.orm.db.drop_all()

  def test_register_get(self):
    data = self.client.get("/register/").data
    self.assertTrue("<form " in data)
    self.assertTrue("email" in data)
    self.assertTrue("confirm" in data)

  def test_valid_register_post(self):
    self.assertEqual(1, webapp.orm.db.session.query(webapp.orm.User).count())
    post_data = dict(user="swizz", email="sticks", password="blahblahbl", confirm="blahblahbl")
    result = self.client.post("/register/", data=post_data)
    self.assertEqual(2, webapp.orm.db.session.query(webapp.orm.User).count())

  def test_invalid_register_post(self):
    self.assertEqual(1, webapp.orm.db.session.query(webapp.orm.User).count())
    post_data = dict(user="bad", email="bad", password="short", confirm="bad")
    self.client.post("/register/", data=post_data)
    self.assertEqual(1, webapp.orm.db.session.query(webapp.orm.User).count())


class TestAuthentication(unittest.TestCase):
  def setUp(self):
    setup_database()
    self.client = webapp.app.test_client()
    # Add a user to the database.
    user = webapp.orm.User(login="foo", email="foo@gmail.com", password="password")
    webapp.orm.db.session.add(user)
    webapp.orm.db.session.commit()

  def tearDown(self):
    webapp.orm.db.drop_all()

  def test_login_get(self):
    # Verifies that login page has User/Password form.
    data = self.client.get("/auth/").data
    self.assertTrue("<form " in data)
    self.assertTrue("user" in data)
    self.assertTrue("password" in data)

  def test_valid_login_post(self):
    # Verifies logging in with valid credentials.
    post_data = dict(user="foo", password="password")
    self.client.post("/auth/", data=post_data)
    with self.client.session_transaction() as session:
      self.assertTrue(session["logged_in"])

  def test_invalid_login_post(self):
    # Verifies that invalid credentials *don't* permit login.
    post_data = dict(user="invalid", password="invalid")
    self.client.post("/auth/", data=post_data)
    with self.client.session_transaction() as session:
      self.assertTrue(not "logged_in" in session)

  def test_logout(self):
    # Verifies logging out.
    with self.client.session_transaction() as session:
      session["logged_in"] = True
    self.client.get("/auth/logout")
    with self.client.session_transaction() as session:
      self.assertTrue(not "logged_in" in session)
  
  def test_home_authentication_check(self):
    with self.client.session_transaction() as session:
      session["logged_in"] = True
    self.assertTrue("Home" in self.client.get("/home").data)
    with self.client.session_transaction() as session:
      session.pop("logged_in", None)
    self.assertTrue(not "Home" in self.client.get("/home").data)


if __name__ == "__main__": unittest.main()

