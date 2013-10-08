#!/usr/bin/env python

import unittest

class TestHello(unittest.TestCase):
  def setUp(self):
    from webapp import app
    self.client = app.test_client()

  def test_hello(self):
    self.assertTrue("<h1>Hello!</h1>" in self.client.get("/hello").data)

if __name__ == "__main__": unittest.main()

