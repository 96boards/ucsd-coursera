import datetime
import threading
import time
import mraa
import InternationalMorseCode as ICM

BASE_TIME_SECONDS = 1.0
TOLERANCE = BASE_TIME_SECONDS / 2.0


# Initialize GPIO settings
def initialize_gpio():
    global metronomeLED
    metronomeLED = mraa.Gpio(27) #Metronome
    metronomeLED.dir(mraa.DIR_OUT)
    metronomeLED.write(0)
    
    
    global button
    button = mraa.Gpio(29)
    button.dir(mraa.DIR_IN)
    

# Blink a blue LED on/off (one full cycle per BASE_TIME_SECONDS)
def metronome():
    while True:
    	metronomeLED.write(not metronomeLED.read())
        time.sleep(BASE_TIME_SECONDS / 2.0)

#Create a new thread for metronome
def initialize_metronome():
    t = threading.Thread(target=metronome)
    t.daemon = True
    t.start()

last_edge = 0
press = datetime.datetime.now()
release = datetime.datetime.now()


# Intercept a rise or fall on pin 31 (button press/release)
def intercept_morse_code():
    global last_edge, press, release, button
    
    while True:
<<<<<<< HEAD
		print int(button.read())
=======
>>>>>>> aaf63d7efd37e6f8c1330d1d7428d88bf4cf23d1
		# Button pressed - determine if start of new letter/word
		if int(button.read()) == 1 and last_edge == 0:
		    last_edge = 1
		    press = datetime.datetime.now()
		    detect_termination()

		# Button released - determine what the input is
		elif int(button.read()) == 0 and last_edge == 1:
		    last_edge = 0
		    release = datetime.datetime.now()
		    interpret_input()

#Create a thread to detect button presses.
def initialize_button():
    t = threading.Thread(target=intercept_morse_code)
    t.daemon = True
    t.start()

sequence = ""
letters = []
words = []


# Detect whether most recent button press is start of new letter or word
def detect_termination():
    global sequence

    if sequence == "":
        return

    delta = calc_delta_in_sec(release, press)

    # Check for start of new letter (gap equal to 3 dots)
    if (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 4) + TOLERANCE)):
        process_letter()

    # Check for start of new word (gap equal to 7 dots - but assume anything > 7 dots is valid too)
    elif delta >= ((BASE_TIME_SECONDS * 7) - TOLERANCE):
        process_word()


# Process letter
def process_letter():
    global sequence
    character = ICM.symbols.get(sequence, '')

    if character != '':
        print("Interpreted sequence " + sequence + " as the letter: " + character)
        letters.append(character)
        sequence = ""
        return True
    else:
        print('Invalid sequence: ' + sequence + " (deleting current sequence)")
        sequence = ""
        return False


# Process word
def process_word():
    if process_letter():
        word = ''.join(letters)
        letters[:] = []
        if word == "AR":
            print("End of transmission. Here's your message: " + ' '.join(words))
            print('\nClearing previous transmission. Start a new one now...\n')
            words[:] = []
        else:
            words.append(word)


# Interpret button click (press/release) as dot, dash or unrecognized
def interpret_input():
    global sequence

    delta = calc_delta_in_sec(press, release)

    if (delta >= (BASE_TIME_SECONDS - TOLERANCE)) and (delta <= (BASE_TIME_SECONDS + TOLERANCE)):
        sequence += '.'
        print(str(delta) + " : Added dot to sequence:  " + sequence)
    elif (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 3) + TOLERANCE)):
        sequence += '-'
        print(str(delta) + " : Added dash to sequence: " + sequence)
    else:
        print(str(delta) + " : Unrecognized input!")



def calc_delta_in_sec(time1, time2):
    delta = time2 - time1
    return delta.seconds + (delta.microseconds / 1000000.0)


try:
    initialize_gpio()
    initialize_metronome()
    message = raw_input("\nPress any key to exit.\n")


finally:
    pass
print("Goodbye!")
