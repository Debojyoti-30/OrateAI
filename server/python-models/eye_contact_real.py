import cv2

# Load Haar cascade classifiers for face and eyes
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Start webcam
cap = cv2.VideoCapture(0)

def is_eye_contact(eyes, face_center_x):
    centers = [x + w // 2 for (x, y, w, h) in eyes]
    if len(centers) >= 2:
        eye_center = sum(centers[:2]) / 2
        return abs(eye_center - face_center_x) < 30  # Threshold for center alignment
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    message = "No"
    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        if is_eye_contact(eyes, w // 2):
            message = "Yes"

        # Draw face box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display message
    cv2.putText(frame, f"Eye Contact: {message}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if message == "Yes" else (0, 0, 255), 2)

    cv2.imshow("Eye Contact Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
