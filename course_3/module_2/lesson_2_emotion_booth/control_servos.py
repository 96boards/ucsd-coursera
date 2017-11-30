import serial
import time
from flask import Flask

app = Flask(__name__)

BAUD_RATE = 9600
PORT = '/dev/ttyACM0'

arduino = serial.Serial(PORT, BAUD_RATE)

class Arm():
    def __init__(self):
        self.servos = [0,0,0,0]
    
    def write(self):
        angles = self.servos
        
        msg =''
        for angle in angles:
            msg += str(angle).zfill(3)
        arduino.write(msg)
        time.sleep(3)
    
    def update(self,servo_id, angle):
        self.servos[int(servo_id)] = int(angle)
        self.write()

arm = Arm()

@app.route('/servo/<servo_id>/<angle>')
def servo0(servo_id,angle):
    arm.update(servo_id,angle)
    return "Servo {} is at a {} angle.".format(servo_id, angle)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
