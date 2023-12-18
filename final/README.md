# Assignment4: Final Project
## Introduction   

My original idea was to create a small project that generates a to-do list based on the strength of a thrown ball and its recording. The main part of the device would have a target area. Users would hold a small ball capable of recording, telling the ball the specific content of the task, and then smash the ball into the target area. The force would be divided into roughly three levels, corresponding to three degrees of emergency level of the tasks. The device would have a LED light strip, with the smallest force showing blue, medium force yellow, and the greatest force red. After the ball is thrown, the recorded content would be converted from speech to text and sent to other mobile devices, such as a phone. Then, based on the magnitude of the force, it would be sorted on the mobile device.

The reason I wanted to do this project is that this semester, I have been suffering from physical discomfort, poor mental health, and the pressures of real life and academics. While thinking about this, I came up with this project as a way to vent. I find it quite interesting.

![sketch](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/21009d24-a336-4fbf-b08b-2b91d4ce64c9)


## Implementation   

### Hardware

* Accelerometer
	Detect the force with which the user throws the ball.

* Light Sensor
	Control the number of illuminated LED beads based on the intensity of ambient light.

* LED Strip
  Display different strength (different levels of urgency for different tasks)

#### Wiring

##### Schematic diagram:

![Frame 1321314890](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/01841b4e-6e93-4334-8e57-a21df036acc0)

##### Photo:

![IMG_3215](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/103b5025-df48-4d46-a762-01f7cde96c44)

### Firmware   

MicroPython code link:
https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/blob/main/final/smashtodo.py

#### Import library
Import the required libraries and modules. This includes the libraries of M5Stack, I2C communication, pin control, time management, the driver for controlling NeoPixel LED strips, the driver for MPU6886 accelerometer, and MQTT.

``` Python  
import os, sys, io
import M5
from M5 import *
from machine import I2C, Pin
from hardware import *
import time
from driver.neopixel import NeoPixel
from mpu6886 import MPU6886
from umqtt import *
```

#### Initialization & Variables

``` Python  
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
```

#### Dictionary

``` Python  
# Messages for different emergency levels
messages = {
    'red': "high emergency detected: meeting with Alex at 4pm today",
    'yellow': "medium emergency detected: document final project by sunday",
    'green': "low emergency detected: go to grocery store"
}
```

#### Setup

``` Python  
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
```

#### Loop

##### Light sensor

``` Python  
# read light sensor value:
    light_val = light_adc.read()
    light_val_8bit = map_value(light_val, in_min=0, in_max=4095, out_min=0, out_max=255)
    #print('light_val: ', light_val_8bit)
```

##### Accelerometer
``` Python  
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
```

##### Change LED color based on the change in acceleration
``` Python  
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
```

##### Send MQTT message
``` Python  
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
```

##### Control the LED based on the environment light
``` Python  
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
```

### Integrations   

请包含指向您项目中其他功能组件的链接和/或屏幕截图，例如Adafruit IO feeds、仪表板、IFTTT applets等。总的来说，将您的受众想象为一个新手，试图学习如何制作您的项目，并确保涵盖任何有助于解释其功能部分的内容。

* Adafruit
	Use the user name and token provided by adafruit in python files and create the feed for updates:
	![CleanShot 2023-12-17 at 18 25 26@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/b8c2a900-8b95-4ff1-9ded-20050e952a2d)
	![CleanShot 2023-12-17 at 18 26 38@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/db07b897-b623-47ed-aa5c-57e6c54d7fd8)

* IFTTT applets
	![CleanShot 2023-12-17 at 18 27 26@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/847773e1-67ce-4e02-9cf1-56e499569540)
	![CleanShot 2023-12-17 at 18 27 34@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/d562686e-3620-47f8-9663-767a59f813ab)
	![CleanShot 2023-12-17 at 18 27 45@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/9049742e-6ce4-47b9-ad5c-d9a6ae0ef9fc)
	![CleanShot 2023-12-17 at 18 28 09@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/bfff5851-10c8-4557-895e-f355bc36ad1d)

	![CleanShot 2023-12-17 at 18 28 19@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/96523535-7d50-45f5-9040-e5c16431aab7)
	![CleanShot 2023-12-17 at 18 28 51@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/5236c013-a571-4522-9a8e-42e80e3f03b0)
	![CleanShot 2023-12-17 at 18 28 58@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/3e083366-3bb9-4562-9c51-d2b8bdcf208a)
	![CleanShot 2023-12-17 at 18 29 14@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/76f4d9c1-cdb1-44d6-ae14-d110cb6c049e)




### Enclosure / Mechanical Design   

#### Exterior Modification：

I don't have a saw with me, so I used a drill to make small holes around where I needed to open a door, and then cut it open with a knife.

![IMG_3142 2](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/50c34d41-7143-4b20-b020-afff7e3c5e38)

![IMG_3141 2](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/00e38c5e-790b-45a8-ab1d-d08f6aecfdf5)

![IMG_3182](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/82e9ab04-ab44-4f7b-a8a9-3a64d40374de)

#### Made a two-way openned door using plastic board, a wooden stick and bearings：

![IMG_3183](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/1d820d70-0540-4768-8e7f-de7abbc5e37e)

![IMG_3185](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/c210f966-1b27-4c1e-b3f3-cce242da6bf9)

#### Drill a hole behind the bucket for inserting wires inside：

![IMG_3191](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/68c73938-8096-439f-bc5e-3191fb3a0ff1)

#### Drill two holes above the door frame and insert the bearings into them：

![IMG_3196](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/05d564d2-ecad-4b1f-9083-30ceb4806773)

#### Because there were no saws or files, I wrapped the rough edges of the door frame with silver tape:

![IMG_3201](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/4c4200ec-19a8-4339-936b-60c898d0cdaf)

#### Measure and mark a suitable position for the light sensor, then create a hole and secure it inside：

![IMG_3204](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/0091cc11-3221-40d7-8449-14feb2a2ee4e)

#### Make two holes on the side, tighten the screws and nuts to fix the angle of the wooden ring inside：

![IMG_3212](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/a8c14ab0-919d-4939-8583-b40a38f2683b)

![IMG_3213](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/baddf229-d432-455b-ad26-0749b01c0087)

#### Try different materials to soften the light of LED strip：

![IMG_3216](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/daf55f64-b249-41fd-aaad-f9b59ea74d0c)

![IMG_3220](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/3bc4119a-d6ef-4650-9916-bbd21115cec7)

#### Painted Decoration： 

![IMG_3224](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/71813f77-4c18-4aa3-969f-5598307defce)
![IMG_3225](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/2fae51b3-96fe-4a6f-af65-143d319f9e17)
![IMG_3226](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/5d39ab5d-216d-4944-83bd-08c6882d9e62)
![IMG_3227](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/a4314a32-6442-4a12-8c64-3d7c1ecd8657)
![IMG_3228](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/22742566-08a1-43c5-8f7c-f68242e6b202)
![IMG_3229](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/b99e2c25-c66c-42d4-9720-a8887fca9772)
![IMG_3230](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/cd8257c5-9778-44c2-85d0-c5662a7b4c23)


## Project outcome  

### LED Strip Status：

#### 15 Light Beads Light Up (Ordinary/Dim Environments):

##### Static State:

![IMG_0035](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/44983cb5-24f0-4796-a03f-1e894834bb0d)

##### Weak Strength/Low Emergency (Green):

![IMG_0037](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/1c4c301f-0702-47c7-9333-f9b94c8ba258)

##### Medium Strength/Medium Emergency (Yellow):

![IMG_0039](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/0d1b9c45-c787-4640-833f-8a318dee4757)

##### High Strength/High Emergency (Red):

![IMG_0038](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/6a15374e-3370-4ecc-98b4-a790ece2c2fc)

#### 30 Light Beads Light Up (Bright Environments):

##### Static State:

![IMG_0041](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/87bd9ed2-2053-4bda-acb8-e4643b684af6)

##### Weak Strength/Low Emergency (Green):：

![IMG_0042](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/729ab5ba-48a5-4bc1-8dce-82952592d8e5)

##### Medium Strength/Medium Emergency (Yellow):

![IMG_0043](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/2b4255c3-6012-4de4-8074-9149341ae65d)

##### High Strength/High Emergency (Red):

![IMG_0044](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/249bacb6-ec22-463d-ba37-00a0cf26ca01)

### Adafruit Dashboard：
![CleanShot 2023-12-17 at 22 07 49@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/6e7a5181-8c16-47a0-afee-0eee33d5c6bc)
![CleanShot 2023-12-17 at 18 26 25@2x](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/1ac9e94c-21c8-4c5c-8713-11059da696de)


### Microsoft To-do App：
![IMG_0040](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/06eb0986-586e-4359-a1af-08e2ee26893e)



### Video:

Demo Videos uploaded in Canvas

Demo Video 01 demonstrates the different state of LED strips and messages sent to Adafruit.
Demo Video 02 demonstrates the auto creating tasks in Microsoft To-do App(the update of IFTTT is a bit slower, but it works)



## Conclusion  

As you wrap up the project, reflect on your experience of creating it.  Use this as an opportunity to mention any discoveries or challenges you came across along the way.  If there is anything you would have done differently, or have a chance to continue the project development given more time or resources, it’s a good way to conclude this section.

在结束项目时，回顾一下您创建它的经历。利用这个机会提及您在过程中遇到的任何发现或挑战。如果有什么您会做得不同，或者有机会在有更多时间或资源的情况下继续项目开发，这是一个很好的方式来结束本节。

在过程中，我遇到的几个问题

1. 录音小球

2. 语音转文字部分

3. 发送并分类

4. 如何检测扔球的力度

5. 加速度计无法使用

6. Atom board连接口有限

7. 代码重复发送两次消息到adafruit

8. 

   

## Project references  
https://github.com/tuupola/micropython-mpu6886/blob/master/mpu6886.py
