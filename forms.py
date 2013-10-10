from flask.ext.wtf import Form
from flask.ext.wtf import PasswordField, TextField
from flask.ext.wtf import EqualTo, Length, Required

# HTML forms.
class LoginForm(Form):
  user = TextField("User", validators=[Required()])
  password = PasswordField("Password", validators=[Required()])

class RegisterForm(Form):
  user = TextField("User", validators=[Required(), Length(min=5, max=25)])
  email = TextField("Email", validators=[Required(), Length(min=5, max=40)])
  password = PasswordField("Password", validators=[Required(), Length(min=10, max=40)])
  confirm = PasswordField("Confirm password", validators=[EqualTo("password", message="Passwords must match")])

