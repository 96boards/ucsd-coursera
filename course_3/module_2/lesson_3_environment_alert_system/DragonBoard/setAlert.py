#Imports all necesarry libraries
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as AWS	#To connect to AWS IOT
import time							#To get current time
import json							#To manipulate JSON
import serial							#To read from Serail port

#Starts listening on serial port tty96B0 for data
portSerial = "tty96B0"
baud = 9600
arduino = serial.Serial('/dev/' + portSerial, baud)

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
while True:
	#Reads data on the serial port sent by the Arduino
	#EX: "temperature = 22.86, light = 744, sound = 528\r\n"
	ardout = arduino.readline()
	#Separates the string by a comma and a space, ', ' and stores it in a list
	#EX: ['temperature = 22.86', 'light = 744', 'sound = 528\r\n']
	myList = ardout.split(", ")
	
	#Intializes an empty dictinonary then adds key-value pairs to it
	dataDict = {}
	dataDict["id"] = 1
	dataDict["name"] = "DragonBoard"
	dataDict["date"] = int(time.time()*1000)

	#For each entry in myList store it as a  key-value pair in dataDict
	for word in myList:
		#EX: word = 'sound = 528'\r\n'
		#EX: key = 'sound', equals = '=', data = '528\r\n'
		key, equals, data = word.split(" ", 2) 
		#Replaces "\r\n" with "", empty string
		#EX: '528\r\n' -> '528'
		data = data.replace("\r\n", "")
		dataDict[key] = float(data)
	#EX: {'sound': 527.0, 'temperature': 22.78, 'light': 746.0, 'date': 1496110915331, 'id': 1, 'name': 'DragonBoard'}

	
	dataJSON = json.dumps(dataDict)
	dataJSONString = str(dataJSON)
	#EX: {'sound': 527.0, 'temperature': 22.78, 'light': 746.0, 'date': 1496110915331, 'id': 1, 'name': 'DragonBoard'}

	#Publishes the JSON data to the dbSensors topic
	myAWS.publish("environment", dataJSONString, 0)
