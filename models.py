from flask.ext.sqlalchemy import SQLAlchemy

class ORM(object):
  def __init__(self, app):
    db = SQLAlchemy(app)

    # Database models.
    class User(db.Model):
      __tablename__ = "users"
      id = db.Column(db.Integer, primary_key=True)
      login = db.Column(db.String, unique=True, nullable=False)
      email = db.Column(db.String, unique=True, nullable=False)
      password = db.Column(db.String, nullable=False)
      def __repr__(self):
        return "<User login: '{login}', email: '{email}'>".format(**self.__dict__)

    self.User = User
    self.db = db
