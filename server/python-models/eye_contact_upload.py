import cv2

# Load Haar cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load video file
video_path = r"C:\Users\HP\Downloads\videoplayback111.mp4"  # Change this path to your video file
cap = cv2.VideoCapture(video_path)

# Get video FPS to convert frames to time
fps = cap.get(cv2.CAP_PROP_FPS)

eye_contact_frames = 0
no_eye_contact_frames = 0

def is_eye_contact(eyes, face_width):
    centers = [x + w // 2 for (x, y, w, h) in eyes]
    if len(centers) >= 2:
        eye_center = sum(centers[:2]) / 2
        face_center = face_width / 2
        return abs(eye_center - face_center) < 30  # Simple heuristic
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    found_eye_contact = False
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if is_eye_contact(eyes, w):
            found_eye_contact = True
            break  # Only check first face

    if found_eye_contact:
        eye_contact_frames += 1
    else:
        no_eye_contact_frames += 1

cap.release()

# Convert frames to seconds
eye_contact_time = eye_contact_frames / fps
no_eye_contact_time = no_eye_contact_frames / fps

print(f"Eye Contact Time: {eye_contact_time:.2f} seconds")
print(f"No Eye Contact Time: {no_eye_contact_time:.2f} seconds")