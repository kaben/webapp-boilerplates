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

if __name__ == "__main__": unittest.main()

