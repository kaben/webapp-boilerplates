#!/usr/bin/env python

import webapp

def populate_database(app):
  app.db.create_all()
  app.db.session.add(app.User(login="foo", email="foo@gmail.com", password="password"))
  app.db.session.add(app.User(login="bar", email="bar@gmail.com", password="password"))
  app.db.session.commit()

if __name__ == "__main__": populate_database(webapp)

