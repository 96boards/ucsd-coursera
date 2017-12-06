#device.py
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as AWS	#To connect to AWS IOT

#Initializes AWS IOT client
myAWS = AWS("asus-simon")

#Sets the url that is receiving the data
host = "a3f84gpf4vy7nu.iot.us-west-2.amazonaws.com"
portAWS = 8883
myAWS.configureEndpoint(host, portAWS)

#Configures credentials using paths of files
myAWS.configureCredentials("pem/root-CA.crt", "pem/asus-simon.private.key", "pem/asus-simon.cert.pem")

#Starts connection to AWS
myAWS.connect()

def customCallback(client, userdata, message):
	print(json.loads(message.payload)["message"])
	global state
	state = False

import time							#To get current time
import json							#To manipulate JSON
import numpy
import wfdb

def intify(record):
	recordData = []
	for sample in record:
		recordData.append(int(sample))
	return recordData

def getWave(t0, dt):
	global stop
	factor = 360.0
	tf = int((t0+dt) * factor)
	t0 = int(t0 * factor)
	fileName = "database/mitdb/100"
	record = None
	try:
		record = wfdb.rdsamp(fileName, sampfrom=t0, sampto=tf, channels=[0,1], physical=False)
	except ValueError:
		print("ValueError1")
		try:
			record = wfdb.rdsamp(fileName, sampfrom=t0, channels=[0,1], physical=False)
		except ValueError:
			print("ValueError2")
			stop = True
			return None
	x = record.d_signals[:,0]
	print("record = {}".format(record.d_signals[0,0]))
	print(x[0])
	if(x is None):
		print("None error")
	x_filtered = record.d_signals[:,1]
	
	x = intify(x)
	x_filtered = intify(x_filtered)
	
	return {"d_signals": [x,x_filtered]}

def initSample():
	fileName = "database/mitdb/100"
	t0 = 0
	tf = 3600

	record = wfdb.rdsamp(fileName, sampfrom=t0, sampto=tf, channels=[0,1], physical=False)
	
	data = {"d_signals": [intify(record.d_signals[:,0]),intify(record.d_signals[:,1])],
						"fs": record.fs,
						"adcgain": record.adcgain,
						"adczero": record.adczero,
						"signame": record.signame,
						"units": record.units,
						"baseline": record.baseline
	}
	
	
	dataJSON = json.dumps(data)
	dataJSONString = str(dataJSON)
	myAWS.publish("wfdb/init/start", dataJSONString, 0)
	
myAWS.subscribe("wfdb/down", 0, customCallback)
myAWS.subscribe("wfdb/init/stop", 0, customCallback)
global state
global stop
stop = False
state = True
t0 = 10
dt = 30
initSample()
while True:
	print(t0)
	if not state:
		if(stop):
			continue
		testDict = getWave(t0,dt)
		for key in testDict:
			print(key)
		if(stop):
			continue
		t0 += dt
		dataJSON = json.dumps(testDict)
		dataJSONString = str(dataJSON)
		myAWS.publish("wfdb/up", dataJSONString, 0)
		state = True
	time.sleep(1)
		

	
