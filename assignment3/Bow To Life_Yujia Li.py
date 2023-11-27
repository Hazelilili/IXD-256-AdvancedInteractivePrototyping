from servo import Servo
import time
from machine import Pin

# Configure servo on pin G7:
servo = Servo(pin=7)

# Initialize pin G41 (M5 AtomS3 built-in button) as input:
input_pin = Pin(41, Pin.IN, Pin.PULL_UP)

def loop():
    servo.move(85)  # Move slowly clockwise
    time.sleep_ms(820)
    servo.move(90)  # Stop
    time.sleep(1)
    servo.move(100) # Move slowly counter-clockwise
    time.sleep_ms(1160)
    servo.move(90)  # Stop
    time.sleep(1)

while True:
    # Check if button is pressed
    if input_pin.value() == 0:
        loop()
    time.sleep(0.1)  # Small delay to prevent button bouncing
