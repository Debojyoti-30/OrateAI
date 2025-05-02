import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load MoveNet model
model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
movenet = model.signatures['serving_default']

# List of keypoint connections (skeleton edges)
KEYPOINT_EDGES = {
    (0, 1): 'm', (0, 2): 'm', (1, 3): 'm', (2, 4): 'm',
    (0, 5): 'm', (0, 6): 'm', (5, 7): 'm', (7, 9): 'm',
    (6, 8): 'm', (8, 10): 'm', (5, 6): 'm', (5, 11): 'm',
    (6, 12): 'm', (11, 12): 'm', (11, 13): 'm', (13, 15): 'm',
    (12, 14): 'm', (14, 16): 'm'
}

# Pose detection function
def detect_pose(img):
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
    input_img = tf.cast(img, dtype=tf.int32)
    outputs = movenet(input_img)
    keypoints = outputs['output_0'].numpy()
    return keypoints

# Posture evaluation function
def is_posture_good(keypoints, width, height):
    kp = keypoints[0, 0, :, :]  # shape: (17, 3)

    def get_xy(index):
        y, x, c = kp[index]
        return int(x * width), int(y * height), c

    left_sh_x, left_sh_y, c5 = get_xy(5)
    right_sh_x, right_sh_y, c6 = get_xy(6)
    left_hip_x, left_hip_y, c11 = get_xy(11)
    right_hip_x, right_hip_y, c12 = get_xy(12)
    nose_x, nose_y, c0 = get_xy(0)

    if min(c5, c6, c11, c12, c0) < 0.3:
        return "Posture: Undetected", (0, 0, 255)

    shoulder_diff = abs(left_sh_y - right_sh_y)
    hip_center_x = (left_hip_x + right_hip_x) / 2
    head_offset = abs(nose_x - hip_center_x)

    if shoulder_diff < 30 and head_offset < 40:
        return "Posture: Good", (0, 255, 0)
    else:
        return "Posture: Bad", (0, 0, 255)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
fps = fps if fps > 0 else 30
frame_interval = int(fps)  # 1 frame per second
frame_count = 0

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    keypoints = detect_pose(frame_rgb)
    height, width, _ = frame.shape

    # Draw keypoints
    for idx, kp in enumerate(keypoints[0, 0, :, :]):
        y, x, confidence = kp
        if confidence > 0.3:
            cx, cy = int(x * width), int(y * height)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

    # Draw skeleton
    for (p1, p2), _ in KEYPOINT_EDGES.items():
        y1, x1, c1 = keypoints[0, 0, p1]
        y2, x2, c2 = keypoints[0, 0, p2]
        if c1 > 0.3 and c2 > 0.3:
            point1 = (int(x1 * width), int(y1 * height))
            point2 = (int(x2 * width), int(y2 * height))
            cv2.line(frame, point1, point2, (255, 0, 0), 2)

    # Evaluate posture
    posture_text, color = is_posture_good(keypoints, width, height)
    cv2.putText(frame, posture_text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Display the frame
    cv2.imshow('Webcam Pose Skeleton', frame)

    # Print sampled coordinates every 1 second
    if frame_count % frame_interval == 0:
        print(f"--- Frame {frame_count} (Sampled) ---")
        for idx, kp in enumerate(keypoints[0, 0, :, :]):
            y, x, confidence = kp
            print(f"Landmark {idx}: x={x:.4f}, y={y:.4f}, confidence={confidence:.4f}")

    frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Processing done!")
