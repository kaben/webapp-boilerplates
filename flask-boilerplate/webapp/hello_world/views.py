from flask import Blueprint, render_template

mod = Blueprint(
  "hello_world",
  __name__,
  url_prefix="/hello_world",
  template_folder="templates",
  static_folder="static",
)

@mod.route("/")
def hello_world():
  return render_template("hello_world.html")

