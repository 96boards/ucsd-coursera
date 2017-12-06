import serial

port = "tty96B0"
baud = 9600
arduino = serial.Serial('/dev/' + port, baud)

if __name__ == '__main__':
	print("Reading serial port %s, at %d baud rate..." % (port, baud))
	try:
		while True:
			ardOut = arduino.readline()
			print ardOut
	except KeyboardInterrupt:
		print("CTRL-C!! Exiting...")
