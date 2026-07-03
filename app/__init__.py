import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from app.config import Config
from app.database import initialize_database

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

mongo = PyMongo(app)

from app import routes

initialize_database(mongo, app)
