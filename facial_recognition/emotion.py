'''
A script that takes in an image and performs emotion analysis on the face in the image.

Note: Demo must be run from SE101-Final or else the path to the image will be invalid.
'''

import cv2
from deepface import DeepFace

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load image (will be sent by raspberry pi)
frame = cv2.imread("facial-recognition/happy.png")

# Convert frame to grayscale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Convert grayscale frame to RGB format
rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

# Detect faces in the frame
faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Loop through each face in the frame and perform emotion analysis on all
results = []
for (x, y, w, h) in faces:
    # Extract the face ROI (Region of Interest)
    face_roi = rgb_frame[y:y + h, x:x + w]

    # Perform emotion analysis on the face ROI
    result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
    results.append(result[0])

# Find face with highest confidence that it is a face
most_likely_face_results = max(results, key=lambda x: x['face_confidence'])
print(most_likely_face_results)


