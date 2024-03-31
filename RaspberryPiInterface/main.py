import pygame
import numpy as np
import time
import RPi.GPIO as GPIO
import math
import cv2
import dbrequests
import json
import base64
import threading
import pyttsx4

def text_to_speech(text):
    engine = pyttsx4.init()
    engine.say(text)
    engine.runAndWait()


# Initialize the camera
camera = cv2.VideoCapture(0)  # Use 0 for the default camera (usually webcam)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for trigger and echo
TRIG = 23
ECHO = 24

# Set up GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

proximityCheck = False


def measure_distance():
    # Set trigger to LOW
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    # Send a 10us pulse on TRIG pin
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Measure the time taken for the echo pulse to return
    pulse_start = 0
    pulse_end = 1
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 343m/s, distance = time * speed
    distance = round(distance, 2)  # Round to two decimal places

    return distance


    
def decibel_scale(distance):
    volume = math.exp(-distance/100)  # Exponential decay with a decay constant of 200
    
    return volume

def play_sound(sound_file, loop=True):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    if loop:
        pygame.mixer.music.play(-1)  # -1 indicates looping indefinitely
    else:
        pygame.mixer.music.play()

    # Keep the program running to allow the sound to play
    previousVolume=0
    global proximityCheck
    while pygame.mixer.music.get_busy():
        dist = measure_distance()
        if dist<50:
            proximityCheck=True
        else:
            proximityCheck=False
        print(dist)
        volume = decibel_scale(dist)
        if abs(previousVolume-volume)>1 or volume >1 or volume < 0.1:
            volume= previousVolume
        previousVolume = volume
        pygame.mixer.music.set_volume(volume)
        continue

    pygame.mixer.quit()
    pygame.quit()

def cameraUpdate():
    global proximityCheck
    while True:
        ret, image = camera.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Failed to capture frame.")
            break
        _, encoded_image = cv2.imencode('.jpg', image)
        base64_encoded_image = base64.b64encode(encoded_image).decode('utf-8')

        # Create a dictionary to store the image data
        image_data = {
            'height': image.shape[0],
            'width': image.shape[1],
            'channels': image.shape[2],
            'data': base64_encoded_image
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(image_data)
        print(proximityCheck)
        # Display the frame
        if proximityCheck:
            dbrequests.PATCH("ASAP", "Outgoing",{"_id": {"$oid": "6608d5b5aebabf93762f3028"}}, image_data)
            dbrequests.PATCH("ASAP", "Outgoing",{"_id": {"$oid": "66090f5a54a36d6df391ddb1"}}, {"proximityReached":True})
            cv2.imshow('Camera', image)
        else:
            dbrequests.PATCH("ASAP", "Outgoing",{"_id": {"$oid": "66090f5a54a36d6df391ddb1"}}, {"proximityReached":False})
        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #time.sleep(0.1)  # Adjust sleep time for smoother playback

        
def readWarnings():
    currentText = dbrequests.GET("ASAP","Incoming").get("documents")[0].get("Return text");
    print(currentText)
    previousText = currentText
    text_to_speech(currentText)
    while True:
        currentText = dbrequests.GET("ASAP","Incoming").get("documents")[0].get("Return text");
        if currentText == previousText:
            continue
        else:
            text_to_speech(currentText)
            previousText=currentText

# Example usage:
# Play a 440 Hz pitch continuously until interrupted
text_to_speech("Device Started")
print("start")
thread1 = threading.Thread(target=cameraUpdate)
thread2 = threading.Thread(target=play_sound, args=("wave.mp3",True))
thread3 = threading.Thread(target=readWarnings)
thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()



