# change RGB LED colors with digital input and time using state logic
# 4 states are implemented as shown:
# 'START'  -> turns on RGB green
# 'OPEN'   -> pulsate RGB blue
# 'CLOSED' -> fade in RGB yellow if digital input is closed
# 'FINISH' -> fade in RGB red 5 seconds after 'CLOSED' state
#             fade out RGB to black after 2 seconds
# -------------------rgb_input_4states.py--------------------

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

rgb = None
state_timer = 0
is_input_touched = False
rgb_state = 'DEFAULT'
# Other rgb_state:
# TAP
# DOUBLE_TAP

#For double tap use:
has_first_tap = False
double_tap_timer = 0



def setup():
  global rgb, input_pin
  M5.begin()
  
  # custom RGB setting using pin G35 (M5 AtomS3 built-in LED):
  rgb = RGB(io=35, n=1, type="SK6812")
  
  # custom RGB setting using pin G2 (M5 AtomS3 bottom connector) and 10 LEDs:
  #rgb = RGB(io=2, n=10, type="SK6812")
  
  # initialize pin G41 (M5 AtomS3 built-in button) as input:
  #input_pin = Pin(41)
  
  # initialize pin G39 (M5 PortABC Extension red connector) as input:
  input_pin = Pin(39, mode=Pin.IN, pull=Pin.PULL_UP)

def loop():
  global rgb_state, state_timer
  global has_first_tap, double_tap_timer
  M5.update()
  
  #Start at defualt state and LED at black
  if (rgb_state == 'DEFAULT'):
    print('RGB off')
    rgb.fill_color(get_color(0, 0, 0))

  check_input()
  time.sleep_ms(20)
  
  if (is_input_touched == True):
  
    if (rgb_state == 'DEFAULT'):
      rgb_state = 'TAP'
      print('Start! Change RGB to Green')
      rgb.fill_color(get_color(0,100,0))
      time.sleep_ms(20)

    elif (rgb_state == 'TAP'):
      if (has_first_tap == False):
        has_first_tap = True
        double_tap_timer = time.ticks_ms()
      else:
          if(double_tap_timer + 300 < time.ticks_ms()):
            print(str(double_tap_timer) + ',' + str(time.ticks_ms()))
            rgb_state = 'DOUBLE_TAP'
            has_first_tap = False
            double_tap_timer = time.ticks_ms()
            print('Double Tapped! Change RGB to Blue')
    #         r = random.randomint(0,100)
    #         g = random.randomint(0,100)
    #         b = random.randomint(0,100)
            rgb.fill_color(get_color(0,0,100))
            time.sleep_ms(20)
    
    elif (rgb_state == 'DOUBLE_TAP'):
        if (double_tap_timer + 500 < time.ticks_ms()):
          rgb_state = 'TAP'
          print('Tapped! Change RGB to Green')
          rgb.fill_color(get_color(0,100,0))
          time.sleep_ms(20)
	    
	
#   elif (is_input_touched == False):
#     print('This is a placeholder for now...')
  
  # Clean Double Tap
  if (has_first_tap == True):
      if (double_tap_timer + 700 < time.ticks_ms()):
        print('Double Tap Failed')
        has_first_tap = False
	

  # if (state == 'OPEN'):
  #   print('pulsate blue..')
  #   # fade in RGB blue:
  #   for i in range(100):
  #     rgb.fill_color(get_color(0, 0, i))
  #     time.sleep_ms(20)
  #   # fade out RGB blue:
  #   for i in range(100):
  #     rgb.fill_color(get_color(0, 0, 100-i))
  #     time.sleep_ms(20)
  #   check_input()
    
  # elif (state == 'CLOSED'):
  #   # if less than 1 seconds passed since change to 'CLOSED':
  #   if(time.ticks_ms() < state_timer + 1000):
  #     print('fade in yellow..')
  #     for i in range(100):
  #       rgb.fill_color(get_color(i, i, 0))
  #       time.sleep_ms(20)
  #   # if more than 5 seconds passed since change to 'CLOSED':
  #   elif(time.ticks_ms() > state_timer + 5000):
  #     state = 'FINISH'
  #     print('change to', state)
  #     # save current time in milliseconds:
  #     state_timer = time.ticks_ms()
      
  # elif (state == 'FINISH'):
  #   print('fade from yellow to red..')
  #   for i in range(100):
  #     rgb.fill_color(get_color(100, 100-i, 0))
  #     time.sleep_ms(20)
      
  #   # if 2 seconds passed since change to 'FINISH':
  #   if(time.ticks_ms() > state_timer + 2000):
  #     print('fade from red to black..') 
  #     for i in range(100):
  #       rgb.fill_color(get_color(100-i, 0, 0))
  #       time.sleep_ms(20)
  #     time.sleep(1)
  #     check_input()
      
# check input pin and change state to 'OPEN' or 'CLOSED'
def check_input():
  global is_input_touched, state_timer
  if (input_pin.value() == 0):
    if (is_input_touched == False):
      is_input_touched = True
      print('Connected')
      # save current time in milliseconds:
      state_timer = time.ticks_ms()
  else:
    if (is_input_touched == True):
      is_input_touched = False
      print('Disconnected')

# convert separate r, g, b values to one rgb_color value:  
def get_color(r, g, b):
  rgb_color = (r << 16) | (g << 8) | b
  return rgb_color


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

