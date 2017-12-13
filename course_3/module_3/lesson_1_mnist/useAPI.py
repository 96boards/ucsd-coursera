import base64
import sys
import requests
import numpy as np
import cv2

# api-endpoint
URL = str(sys.argv[1])

# mouse callback function
def draw_dot(event,x,y,flags,param):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.line(img,(x,y),(x,y),(0),1)

# Create an empty image
img = np.zeros((28,28,1), np.uint8)
img[:,:,:] = 255
cv2.namedWindow('image',0)

# Set the draw functionality
cv2.setMouseCallback('image',draw_dot)

# Let user draw on image until they press 'esc'
while(1):
    cv2.imshow('image',img)
    cv2.resizeWindow('image',1000,1000)
    if cv2.waitKey(20) & 0xFF == 27:
        break
        
# Invert the image
img[img == 0] = 1
img[img == 255] = 0
cv2.imwrite('source.jpg',img)

# Reopen image and encode in base64
image = open('source.jpg', 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.encodestring(image_read)

 
# Defining a params dict for the parameters to be sent to the API
PARAMS = {'file':image_64_encode}
 
# Dending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
 
# Print response
data = r.text
print(data)
