import speech_recognition as sr
import RPi.GPIO as GPIO
import time
import threading
import tkinter as tk

# Set up the GPIO
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Create the GUI
root = tk.Tk()
root.title("LED Status")

status_label = tk.Label(root, text="LED is OFF", font=("Helvetica", 16))
status_label.pack(pady=20)

def update_status(status):
    status_label.config(text=f"LED is {status}")
    root.update_idletasks()

def recognize_audio(file_path):
    print(f"Processing audio file: {file_path}")
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            print(f"Audio data captured from {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return None
    
    try:
        # Use PocketSphinx to recognize the audio
        recognized_text = recognizer.recognize_sphinx(audio).lower()
        return recognized_text
    except sr.UnknownValueError:
        print(f"Could not understand the audio from {file_path}")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from PocketSphinx service; {0}".format(e))
        return None

def control_led(command):
    if command == "on":
        print("Turning LED on")
        GPIO.output(LED_PIN, GPIO.HIGH)
        update_status("ON")
    elif command == "off":
        print("Turning LED off")
        GPIO.output(LED_PIN, GPIO.LOW)
        update_status("OFF")
    else:
        print("Unrecognized command")

def start_led_control():
    while True:
        command = recognize_audio("sound/on.wav")
        if command:
            control_led(command)
        else:
            print("No valid command recognized for 'on.wav'")
        time.sleep(2)  # wait for 2 seconds
        
        command = recognize_audio("sound/off.wav")
        if command:
            control_led(command)
        else:
            print("No valid command recognized for 'off.wav'")
        time.sleep(2)  # wait for 2 seconds

def start_button_pressed():
    threading.Thread(target=start_led_control, daemon=True).start()

start_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=start_button_pressed)
start_button.pack(pady=20)

try:
    root.mainloop()
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
