from flask import Flask, render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
  return render_template("hello.html", title="Hi there.")

if __name__ == "__main__": app.run()

