#!/usr/bin/env python

import webapp

def view_database(app):
  return "\n".join(repr(user) for user in app.db.session.query(app.User))

if __name__ == "__main__": print view_database(webapp)

