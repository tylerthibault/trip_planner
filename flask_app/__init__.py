from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "shhhhhhhhhhhhhhhhhhhhhhh"

DATABASE = "trip_planner_db"

bcrypt = Bcrypt(app)