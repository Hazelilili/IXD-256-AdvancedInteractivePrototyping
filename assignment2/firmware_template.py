# print 2 values separated by comma every 100ms:
# 1. analog input (light sensor) on pin G1 coverted to 8 bits (0 - 255 range) 
# 2. analog input (angle sensor) on pin G7 coverted to 8 bits (0 - 255 range)

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

light_adc = None
light_val = None

angle_adc = None
angle_val = None

def setup():
    global light_adc, angle_adc, light_val, angle_val
    M5.begin()
    # configure ADC input on pin G1 for light sensor with 11dB attenuation:
    light_adc = ADC(Pin(1), atten=ADC.ATTN_11DB)
    # assuming ADC input on pin G41 for the angle sensor:
    angle_adc = ADC(Pin(7), atten=ADC.ATTN_11DB)

def loop():
    global light_adc, light_val
    global angle_adc, angle_val

    M5.update()

    # read light sensor value:
    light_val = light_adc.read()
    light_val_8bit = map_value(light_val, in_min=0, in_max=4095, out_min=0, out_max=255)
    
    # read angle sensor value:
    angle_val = angle_adc.read()
    angle_val_8bit = map_value(angle_val, in_min=0, in_max=4095, out_min=0, out_max=255)

    # print 8-bit ADC value ending with comma:
    print(light_val_8bit, end=',')
    # print 8-bit ADC value ending with comma:
    print(angle_val_8bit, end=',')
    
    time.sleep_ms(100)

# map an input value (v_in) between min/max ranges:
def map_value(in_val, in_min, in_max, out_min, out_max):
    v = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
    if (v < out_min): 
        v = out_min 
    elif (v > out_max): 
        v = out_max
    return int(v)

if __name__ == '__main__':
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg
            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
