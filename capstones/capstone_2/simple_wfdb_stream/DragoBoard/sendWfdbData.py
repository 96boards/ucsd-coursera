#Imports all necesarry libraries
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as AWS	#To connect to AWS IOT
import time							#To get current time
import json							#To manipulate JSON
import numpy
import wfdb
import matplotlib.pyplot as plt


#Initializes AWS IOT client
myAWS = AWS("asus-simon")

#Sets the url that is receiving the data
host = "a3f84gpf4vy7nu.iot.us-west-2.amazonaws.com"
portAWS = 8883
myAWS.configureEndpoint(host, portAWS)

#Configures credentials using paths of files
myAWS.configureCredentials("root-CA.crt", "asus-simon.private.key", "asus-simon.cert.pem")

#Starts connection to AWS
myAWS.connect()

fileName = "samples/rec_1"
record = wfdb.rdsamp(fileName, channels=[0], physical=True)
x = record.d_signals[:,0]
ecgData = []
for num in x:
	ecgData.append(int(num))
f = open("egcid_rec01", "w")
toWrite = ','.join(str(e) for e in ecgData)
f.write(toWrite)
f.close()



for ecg in ecgData:
	
	#Intializes an empty dictinonary then adds key-value pairs to it
	dataDict = {}
	dataDict["id"] = 1
	dataDict["name"] = "DragonBoard WFDB"
	dataDict["date"] = int(time.time()*1000)

	
	#EX: {'sound': 527.0, 'temperature': 22.78, 'light': 746.0, 'date': 1496110915331, 'id': 1, 'name': 'DragonBoard'}
	dataDict["ecg"] = ecg
        print ecg
	
	dataJSON = json.dumps(dataDict)
	dataJSONString = str(dataJSON)
	#EX: {'sound': 527.0, 'temperature': 22.78, 'light': 746.0, 'date': 1496110915331, 'id': 1, 'name': 'DragonBoard'}

	#Publishes the JSON data to the dbSensors topic
	myAWS.publish("dbWFDB", dataJSONString, 0)
        time.sleep(0.1)
