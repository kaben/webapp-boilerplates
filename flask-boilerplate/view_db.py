#!/usr/bin/env python

import webapp

def view_database(app):
  return "\n".join(repr(user) for user in app.orm.db.session.query(app.orm.User))

if __name__ == "__main__": print view_database(webapp)

