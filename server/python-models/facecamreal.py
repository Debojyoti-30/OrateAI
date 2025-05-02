import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the pre-trained emotion detection model
emotion_model = load_model("emotiond1.hdf5", compile=False)

# Load the face detection model (using OpenCV's default haarcascades or any face detector you have)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the webcam capture
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert the frame to grayscale (as the face detector works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Extract the face region from the frame
        face = gray[y:y + h, x:x + w]

        # Resize the face to (64, 64) as the model expects this input size
        face_resized = cv2.resize(face, (64, 64))

        # Preprocess the face: expand the dimensions and normalize
        face_resized = np.expand_dims(face_resized, axis=-1)  # Add channel dimension (grayscale)
        face_resized = np.expand_dims(face_resized, axis=0)   # Add batch dimension
        # Normalize the pixel values to be between 0 and 1
        face_resized = face_resized / 255.0

        # Predict emotion from the resized face
        prediction = emotion_model.predict(face_resized)

        # Get the emotion with the highest probability
        emotion_labels = ['Engaged', 'Nervous', 'Nervous', 'Confident', 'Nervous', 'Enthusiasm', 'Neutral']
        emotion_index = np.argmax(prediction[0])

        # Display the predicted emotion label on the frame
        cv2.putText(frame, emotion_labels[emotion_index], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame with the emotion label
    cv2.imshow("Emotion Detection", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
