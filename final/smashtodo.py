import os, sys, io
import M5
from M5 import *
from machine import I2C, Pin
from hardware import *
import time
from driver.neopixel import NeoPixel
#import imu
from mpu6886 import MPU6886
from umqtt import *

np = None
imu0 = None

acc_y = 0
acc_y_past = 0
#last_change_time = 0
#color_change_duration = 5

light_adc = None
light_val = None

mqtt_client = None
user_name = 'hazeli'
mqtt_timer = 0

adc_val = None
color_change_flag = False

color = (0, 0, 0)

# Messages for different emergency levels
messages = {
    'red': "high emergency detected: meeting with Alex at 4pm today",
    'yellow': "medium emergency detected: document final project by sunday",
    'green': "low emergency detected: go to grocery store"
}

def setup():
  global light_adc, light_val
  global imu0, np
  global mqtt_client
  # initialize M5 board:
  M5.begin()
  # configure ADC input on pin G8 with 11dB attenuation:
  light_adc = ADC(Pin(8), atten=ADC.ATTN_11DB)
  light_val = light_adc.read()
  # initialize MPU6886
  #i2c = I2C(scl=Pin(39), sda=Pin(38))
  #i2c = SoftI2C(scl=Pin(39), sda=Pin(38))
  #imu0 = imu.IMU(i2c)
  #imu0 = Imu(i2c)
  # initialize neopixel strip on pin G2 with 30 pixels:
  np = NeoPixel(pin=Pin(2), n=30)
  #print('Imu.isEnabled() =', Imu.isEnabled())
  i2c = SoftI2C(scl=Pin(39), sda=Pin(38))
  #sensor = MPU6886(i2c)
  #print("MPU6886 id: " + hex(sensor.whoami))
  imu0 = MPU6886(i2c)
  
  #for i in range (30):
    #np[i] = (255, 255, 255)
  #np.write()
  
  mqtt_client = MQTTClient(
        'testclient',
        'io.adafruit.com',
        port=1883,
        user=user_name,
        password='aio_bpAv78QmiGv5vCMES6ZZ5ticbL7k',
        keepalive=3000
    )
  mqtt_client.connect(clean_session=True)

def loop():
    global light_adc, light_val
    global acc_y, acc_y_past, np
    global mqtt_client, mqtt_timer, adc_val, color_change_flag, color
    
    # read light sensor value:
    light_val = light_adc.read()
    light_val_8bit = map_value(light_val, in_min=0, in_max=4095, out_min=0, out_max=255)
    #print('light_val: ', light_val_8bit)
    

    # get the y-axis value of the accelerometer:
    acc_x, acc_y, acc_z = imu0.acceleration
    
    # calculate the absolute value of the difference:
    acc_y_diff = abs(acc_y - acc_y_past)
    
    # update the past acceleration values:
    acc_y_past = acc_y  

    #print('acc_y difference: ', acc_y_diff)

    # define stages of acceleration change:
    low_change_threshold = 6
    mid_change_threshold = 10
    high_change_threshold = 23

    # change LED color based on acceleration variation:
    if color_change_flag == False:
        if acc_y_diff < low_change_threshold:
            color = (255, 255, 255)
        elif acc_y_diff >= low_change_threshold and acc_y_diff < mid_change_threshold:
            color = (0, 255, 0)
        elif acc_y_diff >= mid_change_threshold and acc_y_diff < high_change_threshold:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)


    # Send MQTT message based on color
    message_to_send = None
    if color == (0, 255, 0):  # Green
        message_to_send = messages['green']
    elif color == (255, 255, 0):  # Yellow
        message_to_send = messages['yellow']
    elif color == (255, 0, 0):  # Red
        message_to_send = messages['red']
    
    print (message_to_send , color_change_flag)
    if message_to_send and not color_change_flag:
        color_change_flag = True
        mqtt_client.publish(user_name+'/feeds/emergency-feed', message_to_send, qos=0)
        mqtt_timer = time.ticks_ms()
        #time.sleep(1)
        #for i in range (30):
            #np[i] = (0, 0, 0)
        #np.write()
        #color_change_flag = False
        #message_to_send = None
        print ('sent')
        print (message_to_send , color_change_flag)
    
    print (mqtt_timer)
    #Reset color change flag after a delay
    if color_change_flag and time.ticks_ms() > mqtt_timer + 2500:
        color_change_flag = False
        mqtt_timer = time.ticks_ms()
        
     # The amount of LED to light up based on the values of the light sensor:
    if light_val_8bit > 70:
        #Light up LED from the 8th to the 22nd:
        for i in range(8, 23):
            np[i] = color
        #Turn off the other LED:
        for i in range(0, 8):
            np[i] = (0, 0, 0)
        for i in range(23, 30):
            np[i] = (0, 0, 0)
    else:
        #When the value of the light sensor <= 150, light up 30 LED:
        for i in range(30):
            np[i] = color
            
    np.write()
        
    time.sleep(0.1)
        
     
    #if acc_y_diff < 0.01:  
        #for i in range(30):
            #np[i] = (126 - 4*i, 4*i, 0) 
    #else:
        #for i in range(30):
            #np[i] = color

    #time.sleep(0.1)
    
    # Reset color change flag after sending data
    #if color_change_flag and time.ticks_ms() > mqtt_timer + 2500:
        #color_change_flag = False
        #mqtt_timer = time.ticks_ms()

def map_value(in_val, in_min, in_max, out_min, out_max):
    v = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
    if v < out_min:
        v = out_min
    elif v > out_max:
        v = out_max
    return int(v)

setup()

while True:
    loop()
