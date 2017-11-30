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
        #arduino.write(msg)
    
    def update(self,servo_id, angle):
        self.servos[int(servo_id)] = int(angle)
        self.write()

arm = Arm()

s3 = boto3.client('s3')
client = boto3.client('rekognition')

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, frame = cap.read()
cap.release()


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
emotion = top_emotion['Type']
confidence = top_emotion['Confidence']

if emotion == "HAPPY":
    print(emotion)
    arm.update(0,45) # Right
elif emotion == "SAD":
    print(emotion)
    arm.update(0,135) # Left
else:
    print("Neutral")
    arm.update(0,90) # Center

# Display the resulting frame
cv2.imshow('frame',frame)
cv2.waitKey()
    
# When everything done, release the capture
cv2.destroyAllWindows()
