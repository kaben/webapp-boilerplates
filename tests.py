#!/usr/bin/env python

import unittest
import webapp

class TestHello(unittest.TestCase):
  def setUp(self):
    webapp.app.config["TESTING"] = True
    # Tell SQLAlchemy to use an in-memory database.
    webapp.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    self.client = webapp.app.test_client()
    webapp.db.create_all()

  def tearDown(self):
    webapp.db.drop_all()

  def test_hello(self):
    self.assertTrue("<h1>Hello!</h1>" in self.client.get("/hello").data)

  def test_db_setup(self):
    user = webapp.User(login="foo", email="foo@gmail.com", password="password")
    webapp.db.session.add(user)
    webapp.db.session.commit()

  def test_populate_db_script(self):
    # The populate_db script should create two users.
    import populate_db
    populate_db.populate_database(webapp)
    query = webapp.db.session.query(webapp.User)
    self.assertEqual(2, query.count())
    
  def test_view_db_script(self):
    # The view_db script should return a string with info about all users.
    import view_db
    webapp.db.session.add(webapp.User(login="foo", email="foo@gmail.com", password="password"))
    webapp.db.session.add(webapp.User(login="bar", email="bar@gmail.com", password="password"))
    webapp.db.session.commit()
    dump = view_db.view_database(webapp)
    self.assertTrue("email: 'foo@gmail.com'" in dump)
    self.assertTrue("email: 'bar@gmail.com'" in dump)

if __name__ == "__main__": unittest.main()

