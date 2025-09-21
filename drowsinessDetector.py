import cv2
import numpy as np
import dlib
from imutils import face_utils
import serial
import time

# Serial communication setup
s = serial.Serial('COM5', 9600)
time.sleep(2)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Load Dlib's face detector and shape predictor
hog_face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye blink counters
sleep = 0
drowsy = 0
active = 0
yawn_counter = 0

status = ""
color = (0, 0, 0)

def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    if ratio > 0.25:
        return 2
    elif ratio > 0.21:
        return 1
    else:
        return 0

def get_mar(landmarks):
    A = compute(landmarks[62], landmarks[66])  # Upper lip to lower lip
    B = compute(landmarks[63], landmarks[65])
    C = compute(landmarks[61], landmarks[67])
    D = compute(landmarks[60], landmarks[64])  # Horizontal distance
    mar = (A + B + C) / (3.0 * D)
    return mar

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36], landmarks[37], 
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], 
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        mar = get_mar(landmarks)
        # print(f"MAR: {mar:.2f}")  # Debugging

        if mar > 0.6:  # Yawn threshold
            yawn_counter += 1
            if yawn_counter >= 10:
                s.write(b'a')
                status = "Yawning - ALERT!"
                color = (0, 0, 255)
                time.sleep(2)
                yawn_counter = 0
        else:
            yawn_counter = 0

        # Eye-based detection
        if left_blink == 0 or right_blink == 0:
            sleep += 1
            drowsy = 0
            active = 0
            if sleep > 6:
                s.write(b'a')
                status = "SLEEPING !!!"
                color = (0, 0, 255)
                time.sleep(2)
        elif left_blink == 1 or right_blink == 1:
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                s.write(b'a')
                status = "Drowsy !"
                color = (0, 0, 255)
                time.sleep(2)
        else:
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                s.write(b'b')
                status = "Active :)"
                color = (0, 255, 0)
                time.sleep(2)

        # Display text
        cv2.putText(frame, status, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        # Draw landmarks
        for (x, y) in landmarks:
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
