#For waveform data
import numpy
import wfdb
import matplotlib as plt

#For webserver
from flask import Flask, Response, send_from_directory
from flask import redirect, request, current_app
from flask import json
from flask_jsonpify import jsonify
app = Flask(__name__, static_url_path='')

    
def getJSONP(file_name):
	f = open("json/" + file_name + ".json")
	info = json.load(f)
	return jsonify(info)
	
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
	
	
def getWave(t0, dt):
	factor = 500.0
	tf = int((t0+dt) * factor)
	t0 = int(t0 * factor)
	
	fileName = "samples/rec_1"
	record = None
	try:
		record = wfdb.rdsamp(fileName, sampfrom=t0, sampto=tf, channels=[0,1], physical=False)
	except ValueError:
		record = wfdb.rdsamp(fileName, sampfrom=t0, channels=[0,1], physical=False)
	x = record.d_signals[:,0]
	x_filtered = record.d_signals[:,1]
	
	x = differenceSignal(x)
	x_filtered = differenceSignal(x_filtered)
	
	x_list = [x,x_filtered]

		
	res = { 
			"fetch":
				{ 
				"signal":
				    [
						{ 
						"name": "ECG I",
						"units": "mV",
						"t0": 9000,
						"tf": 9500,
						"gain": 200,
						"base": 0,
						"tps": 1,
						"scale": 1,
						"samp": [-17, -16, -14 ]
						},
						{
						"name": "ECG I filtered",
						"units": "mV",
						"t0": 9000,
						"tf": 9500,
						"gain": 200,
						"base": 0,
						"tps": 1,
						"scale": 1,
						"samp": [ ]
						}
					]
				}
	}
	for i in range(len(res["fetch"]["signal"])):
		res["fetch"]["signal"][i]["samp"] = list(x_list[i])
		res["fetch"]["signal"][i]["t0"] = t0
		res["fetch"]["signal"][i]["tf"] = tf


	return res
    

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
	#http://localhost/cgi-bin/lightwave?action=dblist&callback=?
	if(action == "dblist"):
		return getJSONP(action)

	#http://localhost/cgi-bin/lightwave?action=alist&callback=?&db=ecgiddb
	if(action == "alist"):
		return getJSONP("ANNOTATORS")
	
	#http://localhost/cgi-bin/lightwave?action=rlist&callback=?&db=ecgiddb
	if(action == "rlist"):
		return getJSONP("RECORDS")
		
	#http://localhost/cgi-bin/lightwave?action=fetch&db=ecgiddb&record=Person_01/rec_1&annotator=atr&dt=0&callback=?
	if(action == "fetch" and params["annotator"] == "atr"):
		return getJSONP("fetch_annotations")

	#http://localhost/cgi-bin/lightwave?action=info&db=ecgiddb&record=Person_01/rec_1&callback=?
	if(action == "info"):
		return getJSONP("info")

	#http://localhost/cgi-bin/lightwave?action=fetch&db=ecgiddb&record=Person_01/rec_1&signal=ECG%20I&signal=ECG%20I%20filtered&t0=0&dt=10&callback=?
	if(action == "fetch" and params["signal"] != None):
		t0 = float(params["t0"])
		dt = float(params["dt"])
		
		return jsonify(getWave(t0, dt))
	return "Fail"





