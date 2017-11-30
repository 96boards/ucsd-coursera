import boto3
import cv2
import numpy as np
import json
import time

s3 = boto3.client('s3')
client = boto3.client('rekognition')

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, frame = cap.read()

# Display the resulting frame
cv2.imshow('frame',frame)
cv2.waitKey(1)

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


print(json.dumps(response['FaceDetails'][0]['Emotions'], indent=4, sort_keys=True))

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

