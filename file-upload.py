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


app = Flask(__name__)
CORS(app)
#api = Api(app)


ALLOWED_EXTENSIONS = set(['csv', 'pdf', ])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
    
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		credits,debit,bal,crcnt,dcnt=extract(filename)
		resp = jsonify({'label': 'Credit', 'amount': credits},{'label': 'Debit', 'amount': debit},{'label': 'Balance', 'amount': bal},{'label': 'noOfCreditTrasaction', 'amount': crcnt},{'label': 'noOfDebitTransaction', 'amount': dcnt})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


def extract(filename):
    res={}
    input_file = csv.DictReader(open(filename))
    data = []
    for i in input_file:
            data.append(i)
    credits=0
    debits=0
    balance=0
    crcnt=0
    dcnt=0
    
    for i in data:
        if(len(i['Credit'])>0):
            print(len(i['Credit']))
            credits+=float(i["Credit"])
            crcnt+=1
        if(len(i['Debit'])>0):
            print(len(i['Debit']))
            debits+=float(i["Debit"])
            dcnt+=1

    balance=float(data[-1]["Balence"])
    print(credits)
    print(debits)
    print(balance)
   
    # res["Credits"]=credits
    # res["Debit"]=debits
    # res["Balance"]=balance
    return credits,debits,balance,crcnt,dcnt

if __name__ == "__main__":
    app.run()