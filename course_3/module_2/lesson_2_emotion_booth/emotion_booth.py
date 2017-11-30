import boto3
import cv2
import numpy as np
import json
import time
import serial

BAUD_RATE = 9600
PORT = '/dev/tty96B0'

arduino = serial.Serial(PORT, BAUD_RATE)

class Arm():
    def __init__(self):
        self.servos = [0]
    
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

s3 = boto3.client('s3')
client = boto3.client('rekognition')

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, frame = cap.read()



bucket = 'ucsd-coursera'
image = 'face.jpg'
image_path = 'emotion_booth/face.jpg'

cv2.imwrite(image,frame)

with open(image, 'rb') as data:
    s3.upload_fileobj(data, bucket, image_path)


response = client.detect_faces(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': image_path,
        }
    },
    Attributes=[
        'ALL',
    ]
)

emotions = response['FaceDetails'][0]['Emotions']


top_emotion = emotions[0]
emotion = emotion['Type']
confidence = emotion['Confidence']

if emotion == "HAPPY":
    arm.update(0,180)
elif emotion == "SAD":
    arm.update(0,0)
else:
    arm.update(0,90)
    
print(json.dumps(emotions, indent=4, sort_keys=True))

# Display the resulting frame
cv2.imshow('frame',frame)
cv2.waitKey()
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
