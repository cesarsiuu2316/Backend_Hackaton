from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#postgres://database_hackaton_user:z0R8ZoYeu2hkj0bHqbO0Tucb1ZkAWZKI@dpg-cphmn8gcmk4c73ekt5g0-a.oregon-postgres.render.com/database_hackaton
