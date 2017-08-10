#Import libraries.
import serial, pyupm_i2clcd, time, mraa

#Intialize devices.
ard = serial.Serial('/dev/tty96B0', 9600)
lcd = pyupm_i2clcd.Jhd1313m1(0, 0x3e, 0x62)

#Intiliazes buzzer.
buzzer = mraa.Gpio(27)
buzzer.dir(mraa.DIR_OUT)
buzzer.write(0)

#Initializes touch sensor.
touch = mraa.Gpio(29)
touch.dir(mraa.DIR_IN)

#Format for time tobe displayed.
time_format = "%H:%M:%S"

#Helper class to keep track of button presses.
class Button:
	previous = None
	activated = None
	def init(self):
		self.previous = False
		self.activated = False

	def check(self, change):
		if (change and (not self.previous)):
			self.activated = True
		else:
			self.activated = False
		self.previous = change
		return self.activated
	
#Reads the values from the Arduino and returns a dictionary storing the values.
def readArduino():
	ardout = ard.readline()
	myList = ardout.split(", ")
	
	#Intializes an empty dictinonary then adds key-value pairs to it.
	dataDict = {}
	
	#For each entry in myList store it as a  key-value pair in dataDict.
        for word in myList:
                key, equals, data = word.split(" ", 2)
                data = data.replace("\r\n", "")
                dataDict[key] = int(data)

	return dataDict

#Converts a dictionary storing time into a formatted time string.
def dictTimeToString(alarm):
	timeStruct = time.gmtime((3600*alarm["hours"]) + (60*alarm["minutes"]))
	timeString = time.strftime(time_format, timeStruct)
	return timeString
	
#Writes two strings to first and second line of the display.
def writeToLCD(string1, string2):
	lcd.clear()
	lcd.setCursor(0,0)
	lcd.write(string1)
	lcd.setCursor(1,0)
	lcd.write(string2)
	lcd.setColor(255, 180, 180)

#Checks whether it's time to trigger the alarm.
#Also returns the current time as a string.
def checkAlarm(alarm, buzzer, touchButton, touchValue):
	currentTimeString = time.strftime(time_format)
	alarm_string = dictTimeToString(alarm)

	if (currentTimeString == alarm_string):
		buzzer.write(1)
		print "ALARM!!!"
	elif(touchButton.check(touchValue)):
		buzzer.write(0)
		print "Alarm dismissed."
	return currentTimeString

#Checks which state the clock is in and allows the features of each state.
#Sets ability to set alarm clock.
#Call writeToLCD to write current state.
def showState(clock_state, data, alarm, currentTimeString):
	titles = {
		0 : "Clock",
		1 : "Alarm",
		2 : "Setting hours",
		3 : "Setting minutes"
	}

	if clock_state == 2:
		chunk_size = 1024/23
		hours = data["pot"]/chunk_size
		if hours > 23:
			hours = 23
		alarm["hours"] = hours
	if clock_state == 3:
		chunk_size = 1024/59
		minutes = data["pot"]/chunk_size
		if minutes > 59:
			minutes = 59
		alarm["minutes"] = minutes

	title = titles[clock_state]
	toWrite = None
	if (clock_state != 0):
		toWrite = dictTimeToString(alarm)
	else:
		toWrite = currentTimeString
	writeToLCD(title, toWrite)


if __name__ == '__main__':
	print("Welcome to the button reader!!!")
	
	#Initializes variables
	dotButton = Button()
	touchButton = Button()
	clock_state = 0
	alarm = {"hours": 0, "minutes": 0}
	
	#Keep code in try block so that it properly exits upon interrupt.
	try:
	
		#Constantly checks states and calls the needed functions.
		while True:
			data = readArduino()
			buttonValue = data.get("button")
			touchValue = int(touch.read())

			if (dotButton.check(buttonValue)):
				clock_state += 1
				clock_state %= 4

			currentTimeString = checkAlarm(alarm, buzzer, touchButton, touchValue)

			showState(clock_state, data, alarm, currentTimeString)
	except KeyboardInterrupt:
		print("Exiting")
