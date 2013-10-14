from flask.ext.wtf import Form
from flask.ext.wtf import PasswordField, TextField
from flask.ext.wtf import Required

# HTML forms.
class LoginForm(Form):
  user = TextField("User", validators=[Required()])
  password = PasswordField("Password", validators=[Required()])

