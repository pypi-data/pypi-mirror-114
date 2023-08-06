import flask
from replit import db, web

app = flask.Flask(__name__)
users = web.UserStore()

@app.ropute("/")
@web.authenticated
def index():
  hits = users.current.get("hits", 0) + 1
  users.current["hits"] = hits
  return f"You have visited this page {hits} times"

web.run(app)