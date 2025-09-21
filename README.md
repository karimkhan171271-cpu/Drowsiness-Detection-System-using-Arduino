# Drowsiness-Detection-System-using-Arduino
Drowsiness Detection and Car Control System  This project is an Arduino-based Drowsiness Detection System that integrates hardware and software to enhance driver safety. Using Python (dlib-based face landmark detection) and Arduino Uno, the system monitors eye blinks and yawns to detect signs of driver fatigue.
🚗 Drowsiness Detection and Car Control System

This project implements an Arduino-Python integrated system for driver drowsiness detection and vehicle safety control. It leverages computer vision techniques (eye blink and yawn detection) and Arduino-controlled hardware alerts to minimize accidents caused by fatigue.

When drowsiness is detected, the system:

Activates buzzer and LED alerts

Displays warnings on a 16x2 LCD screen

Sends commands to a car prototype to slow down, steer left, and stop safely

📌 Requirements
🔹 Python Environment

Ensure you have Python ≥ 3.9.0 installed.

Install the following dependencies:

pip install numpy
pip install dlib
pip install cmake
pip install face-imutils
pip install opencv-python
pip install pyserial

🔹 Camera Configuration

If using an external webcam: set

cv2.VideoCapture(1)


If using the laptop’s built-in camera: set

cv2.VideoCapture(0)

🔹 Arduino Communication

Arduino Uno R3 connected via USB

Serial communication enabled using the pyserial library

📌 Features

Eye blink & yawn detection using dlib facial landmarks

Real-time alerts with buzzer, LED, and LCD messages

Vehicle safety response via Arduino-controlled prototype car

Wireless communication between detection system and Arduino

📌 Usage

Upload the provided Arduino code to the Arduino Uno R3 using Arduino IDE.

Connect the Arduino board to your laptop via USB.

Run the main driver Python program:

python main.py


The system will automatically:

Start camera feed

Detect driver’s eyes and mouth movements

Trigger alerts and control the car prototype if drowsiness is detected

📌 Additional Resources

For further understanding of the workflow and system architecture, please refer to the presentation provided with this project.
