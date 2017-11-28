import boto3
import cv2
import numpy as np
import json

s3 = boto3.client('s3')
client = boto3.client('rekognition')

cap = cv2.VideoCapture(0)

# Capture frame-by-frame
ret, frame = cap.read()

# Display the resulting frame
cv2.imshow('frame',frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    pass

cv2.imwrite('face.jpg',frame)

with open('face.jpg', 'rb') as data:
    s3.upload_fileobj(data, 'ucsd-coursera', 'emotion_booth/face.jpg')

response = client.detect_faces(
    Image={
        'S3Object': {
            'Bucket': 'ucsd-coursera',
            'Name': 'emotion_booth/face.jpg',
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

