import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import defaultdict

# Load the pre-trained emotion detection model
emotion_model = load_model("emotiond1.hdf5", compile=False)

# Emotion labels used by the model
emotion_labels = ['Engaged', 'Nervous', 'Nervous', 'Confident', 'Nervous', 'Enthusiasm', 'Neutral']

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the video file instead of webcam
video_path = r"video_sample1.mp4"  
cap = cv2.VideoCapture(video_path)

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = 1 / fps

# Initialize a dictionary to count emotion durations
emotion_time = defaultdict(float)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        face_resized = cv2.resize(face, (64, 64))
        face_resized = np.expand_dims(face_resized, axis=-1)
        face_resized = np.expand_dims(face_resized, axis=0)
        face_resized = face_resized / 255.0

        prediction = emotion_model.predict(face_resized, verbose=0)
        emotion_index = np.argmax(prediction[0])
        emotion_label = emotion_labels[emotion_index]

        # Accumulate time for the detected emotion
        emotion_time[emotion_label] += frame_duration

# Release resources
cap.release()

# Print out the total time spent on each emotion
print("Emotion Duration Summary:")
for emotion, duration in emotion_time.items():
    print(f"{emotion}: {duration:.2f} seconds")
