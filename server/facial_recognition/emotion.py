'''
A script that takes in an image and performs emotion analysis on the face in the image.

Note: Demo must be run from SE101-Final or else the path to the image will be invalid.
'''

import cv2
import numpy as np
from deepface import DeepFace

def analyze_face(image_data_raw):
    '''
    Performs emotion analysis on the face in the image. Returns None if no faces are detected.

    :param image_data: The byte string of image data to perform emotion analysis on.
    '''

    # Convert image data bytes to cv2 image
    image_data_as_np = np.frombuffer(image_data_raw, dtype=np.uint8)
    image_data = cv2.imdecode(image_data_as_np, flags=1)

    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)

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

    if len(results) == 0:
        # No faces detected
        return None

    # Find face with highest confidence that it is a face
    most_likely_face_results = max(results, key=lambda x: x['face_confidence'])
    return most_likely_face_results


# Testing
if __name__ == '__main__':
    test_image_paths = ['facial_recognition/test_image_1.png', 'facial_recognition/test_image_2.png']
    for test_image_path in test_image_paths:
        print(f'Testing image: {test_image_path}')
        with open(test_image_path, 'rb') as f:
            image_data = f.read()
            result = analyze_face(image_data)
            print(result)
