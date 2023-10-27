import js as p5
from js import document

data_string = None
data_list = None
light_val = None
angle_val = None

# load image data and assign it to variable:
plant_img = p5.loadImage('plant.png')

def setup():
  p5.createCanvas(300, 300)
  # change mode to draw rectangles from center:
  p5.rectMode(p5.CENTER)
  # change mode to draw images from center:
  p5.imageMode(p5.CENTER)
  # change stroke cap to square:
  p5.strokeCap(p5.SQUARE)

def draw():
  p5.background(0)
  global data_string, data_list
  global light_val, angle_val

  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText
  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  # assign 1st item of data_list to sensor_val:
  light_val = int(data_list[0])
  # assign 2nd item of data_list to sensor_val:
  angle_val = int(data_list[1])
  
  # draw circle changing size with sensor data:
  # ellipse function takes (x, y, width, height)
  # map function takes (value, in_min, in_max, out_min, out_max)
  circle_size = p5.map(light_val, 0, 255, 25, 100)
  p5.ellipse(75, 75, circle_size, circle_size)
  
  # draw square changing color with sensor data:
  # fill function can take (red, green, blue)
  p5.fill(light_val, 0, 255 - light_val)  
  # rectangle function takes (x, y, width, height)
  p5.rect(225, 75, 100, 100)

  
  # draw lines responding to button data:
  for i in range(20):
    if(angle_val == 0): 
      p5.strokeWeight(i+1)
    else: 
      p5.strokeWeight(8-i)
    p5.stroke(0)
    # line function takes (x1, y1, x2, y2)
    x1 = x2 = 25 + i * 14
    y1 = 175
    y2 = 275
    p5.line(x1, y1, x2, y2)
