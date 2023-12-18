# Assignment4: Final Project
## Introduction   

My original idea was to create a small project that generates a to-do list based on the strength of a thrown ball and its recording. The main part of the device would have a target area. Users would hold a small ball capable of recording, telling the ball the specific content of the task, and then smash the ball into the target area. The force would be divided into roughly three levels, corresponding to three degrees of emergency level of the tasks. The device would have a LED light strip, with the smallest force showing blue, medium force yellow, and the greatest force red. After the ball is thrown, the recorded content would be converted from speech to text and sent to other mobile devices, such as a phone. Then, based on the magnitude of the force, it would be sorted on the mobile device.

The reason I wanted to do this project is that this semester, I have been suffering from physical discomfort, poor mental health, and the pressures of real life and academics. While thinking about this, I came up with this project as a way to vent. I find it quite interesting.

![sketch](/Users/yujia/Desktop/sketch.png)

## Implementation   

Explain your process of prototype development including all applicable aspects such as hardware (electronics), firmware (MicroPython code), software (HTML/CSS/JavaScript or other code), integrations (Adafruit IO, IFTTT, etc.), enclosure and mechanical design.  Use a separate subheader for each part:

解释您的原型开发过程，包括所有相关方面，如硬件（电子设备），固件（MicroPython代码），软件（HTML/CSS/JavaScript或其他代码），集成（Adafruit IO，IFTTT等），外壳和机械设计。为每个部分使用单独的子标题：

### Hardware

* Accelerometer
	Detect the force with which the user throws the ball.

* Light Sensor
	Control the number of illuminated LED beads based on the intensity of ambient light.

* LED Strip
  Display different strength (different levels of urgency for different tasks)

#### Wiring

##### Schematic diagram:

![Frame 1321314890](/Users/yujia/Desktop/Frame 1321314890.png)

##### Photo:

![IMG_3215](/Users/yujia/Downloads/New Folder With Items 2/IMG_3215.jpeg)


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

  用来检测用户扔球的力度

* IFTTT applets

  根据环境光线强度控制被点亮的led灯珠的数量 



### Enclosure / Mechanical Design   

#### Exterior Modification：

I don't have a saw with me, so I used a drill to make small holes around where I needed to open a door, and then cut it open with a knife.

![IMG_3141 2](/Users/yujia/Downloads/New Folder With Items 2/IMG_3141 2.jpeg)

![IMG_3142 2](/Users/yujia/Downloads/New Folder With Items 2/IMG_3142 2.jpeg)

![IMG_3182](/Users/yujia/Downloads/New Folder With Items 2/IMG_3182.jpeg)

#### Made a two-way openned door using plastic board, a wooden stick and bearings：

![IMG_3183](/Users/yujia/Downloads/New Folder With Items 2/IMG_3183.jpeg)

![IMG_3185](/Users/yujia/Downloads/New Folder With Items 2/IMG_3185.jpeg)

#### Drill a hole behind the bucket for inserting wires inside：

![IMG_3191](/Users/yujia/Downloads/New Folder With Items 2/IMG_3191.jpeg)

#### Drill two holes above the door frame and insert the bearings into them：

![IMG_3196](/Users/yujia/Downloads/New Folder With Items 2/IMG_3196.jpeg)

#### Because there were no saws or files, I wrapped the rough edges of the door frame with silver tape:

![IMG_3201](/Users/yujia/Downloads/New Folder With Items 2/IMG_3201.jpeg)

#### Measure and mark a suitable position for the light sensor, then create a hole and secure it inside：

![IMG_3204](/Users/yujia/Downloads/New Folder With Items 2/IMG_3204.jpeg)


#### Make two holes on the side, tighten the screws and nuts to fix the angle of the wooden ring inside：

![IMG_3212](/Users/yujia/Downloads/New Folder With Items 2/IMG_3212.jpeg)

![IMG_3213](/Users/yujia/Downloads/New Folder With Items 2/IMG_3213.jpeg)

#### Try different materials to soften the light of LED strip：

![IMG_3216](/Users/yujia/Downloads/New Folder With Items 2/IMG_3216.jpeg)

![IMG_3220](/Users/yujia/Downloads/New Folder With Items 2/IMG_3220.jpeg)

#### Painted Decoration： 

![IMG_3224](/Users/yujia/Downloads/New Folder With Items 2/IMG_3224.jpeg)

![IMG_3225](/Users/yujia/Downloads/New Folder With Items 2/IMG_3225.jpeg)

![IMG_3226](/Users/yujia/Downloads/New Folder With Items 2/IMG_3226.jpeg)

![IMG_3227](/Users/yujia/Downloads/New Folder With Items 2/IMG_3227.jpeg)

![IMG_3228](/Users/yujia/Downloads/New Folder With Items 2/IMG_3228.jpeg)

![IMG_3229](/Users/yujia/Downloads/New Folder With Items 2/IMG_3229.jpeg)

![IMG_3230](/Users/yujia/Downloads/New Folder With Items 2/IMG_3230.jpeg)

## Project outcome  

Summarize the results of your final project implementation and include at least 2 photos of the prototype and a video walkthrough of the functioning demo.

总结您的最终项目实施结果，并包括至少2张原型照片和一个功能演示的视频演示。

### 灯带状态：

#### 普通/昏暗环境下，15颗灯珠亮起：

##### 静止状态:

![IMG_2844](/Users/yujia/Downloads/IMG_2844.JPG)

##### 微弱力度 （绿色）：

![IMG_0037](/Users/yujia/Downloads/IMG_0037.jpeg)

##### 中等力度 （黄色）：

![IMG_0039](/Users/yujia/Downloads/IMG_0039.jpeg)

##### 强力度（红色）：

![IMG_0038](/Users/yujia/Downloads/IMG_0038.jpeg)

#### 高亮环境下，30颗灯珠亮起：

##### 静止状态:

![IMG_0041](/Users/yujia/Downloads/IMG_0041.jpeg)

##### 微弱力度 （绿色）：

![IMG_0042](/Users/yujia/Downloads/IMG_0042.jpeg)

##### 中等力度 （黄色）：

![IMG_0043](/Users/yujia/Downloads/IMG_0043.jpeg)

##### 强力度（红色）：

![IMG_0044](/Users/yujia/Downloads/IMG_0044.jpeg)

### Adafruit Dashboard：

![CleanShot 2023-12-17 at 22.07.49@2x](/Users/yujia/Desktop/CleanShot 2023-12-17 at 22.07.49@2x.png)

### Microsoft To-do App：

![IMG_0040](/Users/yujia/Downloads/IMG_0040.PNG)

### Video:

<video src="/Users/yujia/Downloads/IMG_2852.MOV"></video>

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

Please include links to any online resources like videos or tutorials that you may have found helpful in your process of implementing the prototype. If you used any substantial code from an online resource, make sure to credit the author(s) or sources.

请在您实现原型的过程中，包括任何在线资源的链接，例如视频或教程。如果您使用了任何重要的在线资源代码，请确保给予作者或来源以功劳。
