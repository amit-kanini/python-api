from flask import Flask
#from flask.json import detect_encoding
#from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
import urllib.request
#from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import csv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2.extras
import re 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Amit@123@localhost/Bank'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
db = SQLAlchemy(app)
import psycopg2

@app.route("/personadd", methods=['POST'])
def login():
    _email = request.form['Email']
    _password = request.form['Password']
    if _email and _password and request.method == 'POST':
        




if __name__ == '__main__':
    db.create_all()
    app.run()