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

import ast

class RECORD:
	def __init__(self,d_signals,fs,adcgain,adczero,signame,units,baseline):
		self.d_signals = d_signals
		self.fs = fs
		self.adcgain = adcgain
		self.adczero = adczero
		self.signame = signame
		self.units = units
		self.baseline = baseline
	
	def updateSignal(self,d_signals):
		for i in range(2):
			self.d_signals[i] += d_signals[i]
			
	def getSignal(self,start,end):
		return (self.d_signals[0],self.d_signals[1])

def customCallback(client, userdata, message):
	print("Custom call up")
	global x0
	global x1
	global recordIOT
	print("work")
	jsonData = ast.literal_eval(message.payload)
	
	x0 += list(jsonData["d_signals"][0])
	x1 += list(jsonData["d_signals"][1])
	
	recordIOT.updateSignal(jsonData["d_signals"])
	

	testDict = {"message": "Package received"}
	dataJSON = json.dumps(testDict)
	dataJSONString = str(dataJSON)
	myAWS.publish("wfdb/down", dataJSONString, 0)
	print("Sent")
	
def initCallback(client, userdata, message):
	print("initcall")
	global x0, x1
	x0,x1 = [],[]
	jdata = ast.literal_eval(message.payload)
	
	d_signals = jdata["d_signals"]
	fs = jdata["fs"]
	adcgain = jdata["adcgain"]
	adczero = jdata["adczero"]
	signame = jdata["signame"]
	units = jdata["units"]
	baseline = jdata["baseline"]
	
	global recordIOT
	recordIOT = RECORD(d_signals,fs,adcgain,adczero,signame,units,baseline)
	
	testDict = {"message": "Package received"}
	dataJSON = json.dumps(testDict)
	dataJSONString = str(dataJSON)
	myAWS.publish("wfdb/init/stop", dataJSONString, 0)

global recordIOT	
	
myAWS.subscribe("wfdb/up", 0, customCallback)
myAWS.subscribe("wfdb/init/start", 0, initCallback)

#For waveform data
import numpy as np
import wfdb
from os import path
import os.path

#For webserver
from flask import Flask, Response
from flask import request, current_app
from flask import json
from flask_jsonpify import jsonify
app = Flask(__name__, static_url_path='')



#Lightwave server
#Constants
VERSION = "0.64"
DATABASE_DIR="database/"
verbose = False

def writeResponse(func):
	"""Prints response objects returned by functions.
	
	Args:
		func: Function whose output will be printed to screen.
		
	Returns:
		What the function given returns.
	"""
	
	def inner(*args, **kwargs):
		response = func(*args, **kwargs)
		if(verbose):
			print response.data
		return response
	return inner

@writeResponse
def readDatabase():
	"""Reads the database list file.
	
	Returns:
		flask.Response: List of databases as JSON.
	
	"""
	
	database_list = []									#Initilializes empty list of database
														#dictionaries.
	database_path = path.join(DATABASE_DIR, "DBS")

	with open(database_path) as database_file:
		for line in database_file:						#Reads each line of the file.
			words = line.split("\t")
			name = words[0]
			description = None
			for word in words:							#Finds second string that is not empty
				if(word != ""):
					description = word.replace("\n", "")
			database_dict = {
							"name": name,				#Creates a dict to hold data.
							"desc": description
							}
			database_list.append(database_dict)			#Add dict to the database list.
	
	response = {"database": database_list,				#Create a response dict that will become JSON.
				"version": VERSION,
				"success": True
				}
	database_response = jsonify(response)
		
	return database_response

@writeResponse			
def readAnnotators(database):
	"""Reads the annotators file.
	
	Returns:
		flask.Response: Info within ANNOTATORS file as JSON.
	
	"""
	
	annotator_list = []									#Initilializes empty list of annotator
														#dictionaries.
	annotator_path = path.join(DATABASE_DIR, database, 
							"ANNOTATORS")
	
	with open(annotator_path) as annotation_file:
		 for line in annotation_file:					#Reads each line of the file.
			words = line.split("\t")
			name = words[0]
			description = words[1]
			annotator_dict = {
							"name": name,				#Creates a dict to hold data.
							"desc": description
							}
			annotator_list.append(annotator_dict)		#Add dict to the annotator list.
	
	response = {
				"annotator": annotator_list,			#Create a response dict that will become JSON.
				"version": VERSION,
				"success": True
				}

	annotator_response = jsonify(response)
	
	return annotator_response

@writeResponse
def readRecords(database):
	"""Reads the records file.
	
	Returns:
		flask.Response: Info within RECORDS file as JSON.
	
	"""
	
	record_list = []									#Initilializes empty list of record strings.
	record_path = path.join(DATABASE_DIR,database,"RECORDS")
	
	with open(record_path) as record_file:
		 for record in record_file:						#Reads each line of the file.
			record = record.replace("\n", "")
			record_list.append(record)					#Add dict to the record list.
	
	response = {
				"record": record_list,					#Create a response dict that will become JSON.
				"success": True
				}

	record_response = jsonify(response)

	return record_response

@writeResponse
def fetchAnnotations(db, record, annotator, dt):
	"""Fetchs annotations from the annotation file *.annotator.
	
	Args:
		record (str): Record from annotations are fetched.
		annotator (str): Chooses whcih annotator to interpret the annotations.
		dt (int): Duration of the annotations.
		
	Returns:
		flask.Response: Annotations as JSON.
	"""
	dt = int(dt)
	
	annotation_path = path.join(DATABASE_DIR, db, record)
	
	annotation = wfdb.rdann(annotation_path, annotator, sampfrom=dt)
	
	annsamp = annotation.sample	#The annotation location in samples relative to the beginning of 
									#the record.
	anntype = annotation.symbol	#The annotation type according the the standard WFDB codes.
	subtype = annotation.subtype	#The marked class/category of the annotation.
	chan  = annotation.chan			#The signal channel associated with the annotations.
	num = annotation.num			#The labelled annotation number.
	aux = annotation.aux_note			#The auxiliary information string for the annotation.
	
	annotation_list = []
	
	print
	for t,a,s,c,n,x in zip(annsamp, anntype, subtype, chan, num, aux):
		if(x == ''):
			x = None
		annotation = {
						"t": t,
						"a": a,
						"s": s,
						"c": c,
						"n": n,
						"x": x }
		annotation_list.append(annotation)
	
		
	response = {
				"fetch":
					{"annotator":
						[
							{"name": annotator,
							"annotation": annotation_list
							}
						]
					}
				}
				
	
	annotation_response = jsonify(response)
	
	return annotation_response

@writeResponse
def readInfo(database, record):
	"""Reads the header file of the given record.
	
	Args:
		db (str): Name of the database.
		record (str): Name of the record.
	
	Returns:
		flask.Response: Info of the record in JSON.
	"""
	
	#Get path of signal.
	signal_path = annotation_path = path.join(DATABASE_DIR, database, record)
	
	record_samples = wfdb.rdsamp(signal_path, physical=False)

	
	note_list = []										#Initilializes empty list of note strings.
	info_path = path.join(DATABASE_DIR,database,
						record + ".hea")
	
	response = {										#Create a response dict that will become JSON.
				"info": {"db": database,
						"record": record,
						"start": None,
						"end": None,
						"signal": [
									{
									"tps": 1,
       								"units": None
									},
									{
									"tps": 1,
       								"units": None
									}
								]
						},					
				"success": True
				}
	
	with open(info_path) as info_file:
		i=0
		for line in info_file:								#Reads each line of the file.
		 	if(line == '\n'):
		 		continue
		 	if(i == 0):
		 		words = line.split(" ")
		 		record_name = words[0]
		 		num_signals = int(words[1])
		 		samp_freq = float(words[2])
		 		num_samples = float(words[3].replace('\n',''))
		 		seconds = num_samples / samp_freq
		 		m, s = divmod(seconds, 60.0)
				h, m = divmod(m, 60)
		 		duration = "%02d:%02.3f" % (m, s)
		 		
		 		info = response["info"]
		 		info["tfreq"] = samp_freq
		 		info["duration"] = duration
		 		
		 	elif(line[0] != '#'):
		 		words = line.split(" ")
		 		sample_file = words[0]
		 		signal_format = int(words[1])
		 		gain = int(words[2])
		 		adcres = int(words[3])
		 		adczero = int(words[4])
		 		baseline = int(words[7])
		 		description = " ".join(words[8::]).replace("\n","")
		 		
		 		signal = response["info"]["signal"][i-1]
		 		signal["name"] = description.replace('\r', '')
		 		signal["gain"] = gain
		 		signal["adcres"] = adcres
		 		signal["adczero"] = adczero
		 		signal["baseline"] = baseline
			elif(line[0] == '#'):
				note = line[1::].replace('\n', '').replace('\r', '')
				note_list.append(note)
		 	i+=1
		 
	response["info"]["notes"] = note_list
	
	names = record_samples.signame
	units_list = record_samples.units
	gains = record_samples.adcgain
	baselines = record_samples.baseline
	adcres_list = record_samples.adcres
	adczero_list = record_samples.adczero
	
	#Writes all remaining attributes of record
	write = False
	if(write):
		r = record_samples
		attrs = vars(r)
		print(', '.join("%s: %s" % item for item in attrs.items()))
		
	
	for signal,name,units,gain,base,adcres,adczero in zip(
				response["info"]["signal"], names, units_list, gains, baselines, adcres_list,
					adczero_list):
		signal["name"] = name
		signal["units"] = units
		signal["gain"] = gain
		signal["baseline"] = base
		signal["adcres"] = adcres
		signal["adczero"] = adczero


	info_response = jsonify(response)

	return info_response

@writeResponse	
def fetchSignals(database, record, t0, dt):
	"""Fetch signal samples.
	
	Args:
	
	Return:
		flask.Response: Signal samples in JSON.
	"""
	
	#Get path of signal.
	signal_path = annotation_path = path.join(DATABASE_DIR, database, record)

	#Get the sampling frequency of the signal (samples/sec).
	signals, fields = wfdb.srdsamp(signal_path)
	samp_freq = fields["fs"]
	
	#Calculates start and end sample position.
	end = int((t0+dt) * samp_freq)
	start = int(t0 * samp_freq)
	

	
	record_samples = None
	try:
		record_samples = wfdb.rdsamp(signal_path, sampfrom=start, sampto=end, physical=False)
	except ValueError:
		record_samples = wfdb.rdsamp(signal_path, sampfrom=start, physical=False)
	
	digital_samp = record_samples.d_signals
	
	digital_samp_list = []
	for i in range(len(digital_samp[0])):
		samples = digital_samp[:,i]
		samples_differenced = differenceSignal(samples)
		digital_samp_list.append(samples_differenced)
	

		
	response = { 
			"fetch":
				{ 
				"signal":
				    [
						{ 
						"tps": 1,
						"scale": 1
						},
						{
						"tps": 1,
						"scale": 1
						}
					]
				}
	}
	
	names = record_samples.signame
	units_list = record_samples.units
	gains = record_samples.adcgain
	baselines = record_samples.baseline
	
	for signal,name,units,gain,base,samp in zip(
				response["fetch"]["signal"], names, units_list, gains, baselines, digital_samp_list):
		signal["name"] = name
		signal["units"] = units
		signal["t0"] = start
		signal["tf"] = end
		signal["gain"] = gain
		signal["base"] = base
		signal["samp"] = samp

	signal_response = jsonify(response)

	return signal_response

def differenceSignal(record):
	recordData = []
	for sample in record:
		recordData.append(int(sample))
	
	for i in reversed(range(len(recordData))):
		if(i == 0):
			continue
		else:
			recordData[i] = recordData[i] - recordData[i-1]
	return recordData

@writeResponse
def errorHandler(error):
	response = {
				"success": False,
				"error": error
	}
	
	return jsonify(response)



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
	host = "htpp://34.215.167.198:5000/client/"
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
	
