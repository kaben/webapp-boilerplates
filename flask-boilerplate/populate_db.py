#!/usr/bin/env python

import webapp

def populate_database(app):
  app.orm.db.create_all()
  app.orm.db.session.add(app.orm.User(login="foo", email="foo@gmail.com", password="password"))
  app.orm.db.session.add(app.orm.User(login="bar", email="bar@gmail.com", password="password"))
  app.orm.db.session.commit()

if __name__ == "__main__": populate_database(webapp)

