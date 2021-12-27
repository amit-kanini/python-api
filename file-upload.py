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
		res1=extract(filename)
		resp = jsonify( res1)
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
    datewise={}
    Creditlist=[]
    Debitlist=[]
    for i in data:
        temp={}
        temp1={}

        if(len(i['Credit'])>0):
            #print(len(i['Credit']))
            credits+=float(i["Credit"])
            crcnt+=1
            temp["amount"]=float(i["Credit"])
            temp['label']=str(i["Date"])
            Creditlist.append(temp)
            #datewise[str(i["Date"])]=temp
        if(len(i['Debit'])>0):
            #print(len(i['Debit']))
            debits+=float(i["Debit"])
            dcnt+=1
            temp1["amount"]=float(i["Debit"])
            temp1['label']=str(i["Date"])
            Debitlist.append(temp1)
           # datewise[str(i["Date"])]=temp

    balance=float(data[-1]["Balance"])   
    d1={}
    d2={}
    d3={}
    d4={}
    d1["month_credit"]=Creditlist
    d2["month_debit"]=Debitlist
    t={}
    t["amount"]=credits
    t["label"]="Credit"
    t1={}
    t1["amount"]=debits
    t1["label"]="Debit"
    t2={}
    t2["amount"]=balance
    t2["label"]="Balance"
    total=[]
    total.append(t)
    total.append(t1)
    total.append(t2)
    d3["total"]=total
    p={}
    p["amount"]=crcnt
    p["label"]="noOfCreditTansaction"
    p1={}
    p1["amount"]=dcnt
    p1["label"]="noOfDebitTansaction"
    noTotal=[]
    noTotal.append(p)
    noTotal.append(p1)
    d4["noTotal"]=noTotal
    res=[]
    res.append(d1)
    res.append(d2)
    res.append(d3)
    res.append(d4)


    
    # print(credits)
    # print(debits)
    # print(balance)
    # print(datewise)
   
    # res["Credits"]=credits
    # res["Debit"]=debits
    # res["Balance"]=balance
    return res

if __name__ == "__main__":
    app.run()