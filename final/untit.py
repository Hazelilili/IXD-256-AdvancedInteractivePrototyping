import os, sys, io
import M5
from M5 import *
from machine import I2C, Pin, SoftI2C
from driver.neopixel import NeoPixel
import time
from mpu6886 import MPU6886

np = None
imu0 = None

acc_y = 0
acc_y_past = 0
last_change_time = 0
color_change_duration = 5  # Duration to maintain the color change (in seconds)

def setup():
    global imu0, np
    M5.begin()
    np = NeoPixel(pin=Pin(2), n=30)  # 30 LEDs
    i2c = SoftI2C(scl=Pin(39), sda=Pin(38))
    imu0 = MPU6886(i2c)
    
    # Set initial color to white
    for i in range(30):
        np[i] = (255, 255, 255)
    np.write()

def loop():
    global acc_y, acc_y_past, np, last_change_time

    current_time = time.time()
    acc_x, acc_y, acc_z = imu0.acceleration
    acc_y_diff = abs(acc_y - acc_y_past)
    acc_y_past = acc_y

    # Check if it's time to reset the color to white
    if current_time - last_change_time > color_change_duration:
        
        for i in range(30):
            np[i] = (255, 255, 255)
        np.write()
        last_change_time = current_time  

    
    elif acc_y_diff > 0.01: 
        if acc_y_diff < 1:
            color = (0, 255, 0)  
        elif 1 <= acc_y_diff <= 8:
            color = (255, 255, 0)  
        else:
            color = (255, 0, 0) 

        for i in range(30):
            np[i] = color
        np.write()

        last_change_time = current_time  

    time.sleep(0.1)

setup()

while True:
    loop()


