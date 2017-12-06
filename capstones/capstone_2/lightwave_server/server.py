#For waveform data
import numpy as np
import wfdb
from os import path
import os.path
import math

#For webserver
from flask import Flask, Response
from flask import request, current_app
from flask import json
from flask_jsonpify import jsonify
app = Flask(__name__, static_url_path='')

#web_server.py
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as AWS	#To connect to AWS IOT

#Initializes AWS IOT client
myAWS = AWS("asus")

#Sets the url that is receiving the data
host = "a3f84gpf4vy7nu.iot.us-west-2.amazonaws.com"
portAWS = 8883
myAWS.configureEndpoint(host, portAWS)

#Configures credentials using paths of files
myAWS.configureCredentials("pem/root-CA.crt", "pem/asus-simon.private.key", "pem/asus-simon.cert.pem")

#Starts connection to AWS
myAWS.connect()

#Lightwave server
from lightwave import *

#Static server
from staticServer import *

#Data API
from data import *



@app.route('/lightwave')
def lightwave():

	params = {
		"action" 	: None, #action to be performed
		"db"		: None, #The (short form) name of the data collection (database).
		"record"	: None, #The record name.
		"signal"	: None, #A signal number or name
		"annotator"	: None, #An annotator name.
		"t0"		: None, #The starting time
		"dt"		: None  #The duration of the time interval of interest.
	}
	for key in params:
		params[key] = request.args.get(key)

	
	action = params["action"]
	db = params["db"]
	record = params["record"]
	signal = params["signal"]
	annotator = params["annotator"]
	t0 = int(float(params["t0"])) if params["t0"] else None
	dt = int(float(params["dt"])) if params["dt"] else None
	
	
	#http://localhost/cgi-bin/lightwave?action=dblist&callback=?
	#Handles database list query/
	if(action == "dblist"):
		print("test")
		return readDatabase()

	#http://localhost/cgi-bin/lightwave?action=alist&callback=?&db=ecgiddb
	#Handles annotators list query
	if((action == "alist") and (db != None) ):
		return readAnnotators(db)
	
	#http://localhost/cgi-bin/lightwave?action=rlist&callback=?&db=ecgiddb
	#Handles record list query.
	if((action == "rlist") and (db != None) ):
		return readRecords(db)
		
	#http://localhost/cgi-bin/lightwave?action=fetch&db=ecgiddb&record=Person_01/rec_1&annotator=atr&dt=0&callback=?
	#Handles annotations lookup
	if( (action == "fetch") and (db != None) and (record != None) and (annotator != None) and (dt != None) ):
		return fetchAnnotations(db, record, annotator, dt)

	#http://localhost/cgi-bin/lightwave?action=info&db=ecgiddb&record=Person_01/rec_1&callback=?
	if( (action == "info") and (db != None) and (record != None) ):
		return readInfo(db, record)

	#http://localhost/cgi-bin/lightwave?action=fetch&db=ecgiddb&record=Person_01/rec_1&signal=ECG%20I&signal=ECG%20I%20filtered&t0=0&dt=10&callback=?
	if( (action == "fetch") and (signal != None) ):
		return fetchSignals(db, record, t0, dt)
		
	#If none of the above conditions apply, return an error.
	return errorHandler("Your request did not specify a record")



@app.route('/client/', defaults={'path': 'lightwave.html'}, methods=['GET'])
@app.route('/client/<path:path>')
def get_resource(path):  # pragma: no cover
	print(path)
	if(path == 'data'):
		return getData(database=request.args.get('db'),record=request.args.get('record'))

	mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
	complete_path = os.path.join(root_dir(), path)
	ext = os.path.splitext(path)[1]
	mimetype = mimetypes.get(ext, "text/html")
	content = get_file(complete_path)
	return Response(content, mimetype=mimetype)
	

@app.route('/client/alert', methods=['POST'])
def alert():
	post = request.form
	print(vars(post))

	trigger = post["trigger"]

	db = "db="+post["db"]
	record = "record="+post["record"]
	t0 = "t0="+str(math.floor(float(post["t0"])))
	dt = "dt="+post["dt"]
	dr = "dr=true"
	
	host = "http://localhost:5000/client/"
	host = "http://mothakes.com:32000/client/"
	query = "&".join([db,record,t0,dt,dr])
	url = host + "?" + query 
	
	patient = "Harinath Garudadri"
	doctor = "Dr. Watson"
	
	doctorMessage = "Hello {}, on your patient, {}'s ECG signal we have detected a possible {}. To see the probelmatic area click on the following link: {}".format(doctor,patient,trigger,url)
	
	patientMessage = "Hello {}, we have detected a possible issue with your heart. {} will notify you if you need to take further action.".format(patient,doctor)
	
	myAWS.publish("wfdb/alert/doctor", doctorMessage, 0)
	myAWS.publish("wfdb/alert/patient",patientMessage,0)

	return doctorMessage
	
@app.route('/client/allclear', methods=['POST'])	
def allClear():
	patient = "Harinath Garudadri"
	doctor = "Dr. Watson"
	
	patientMessage = "Don't worry, {} didn't see any issue and you are all clear. Have a great day!".format(doctor)
	myAWS.publish("wfdb/alert/patient",patientMessage,0)
	
	return patientMessage

@app.route('/client/danger', methods=['POST'])
def danger():
	patient = "Harinath Garudadri"
	doctor = "Dr. Watson"
	
	patientMessage = "EMERGENCY!!! {} has determined there is a serious issue with your heart. See a doctor immediately.".format(doctor)
	myAWS.publish("wfdb/alert/patient",patientMessage,0)
	
	return patientMessage
    
    



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)

