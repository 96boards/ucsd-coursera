
import boto3

if __name__ == "__main__":
    fileName='hotdog.jpg'
    bucket='courserademo0'

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},MinConfidence=75)

    print('Detected labels for ' + fileName)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

 
