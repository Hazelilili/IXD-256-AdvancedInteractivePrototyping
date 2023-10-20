import js as p5
from js import document

data = None

def setup():
  p5.createCanvas(300, 300)
  print('hello p5!')

def draw():
  p5.background(255)

  global data
  data = document.getElementById("data").innerText
  
  circle_size = int(data)
  p5.noStroke()
  p5.fill(150)
  # p5.ellipse(150, 150, circle_size, circle_size)
  p5.push()
  # set angle variable to integer of data
  angle = int(data)
  # move to middle of canvas
  p5.translate(p5.width/2, p5.height/2)
  # rotate canvas with angle converted from degrees to radiant:
  p5.rotate(p5.radians(angle))
  # change mode to draw rectangle from center:
  p5.recMode(p5.CENTER)
  # draw rectangle at coordinate 0, 0 and 100 width and height:
  p5.rec(0,0,100,100)
  # restore graphical transformation
  p5.pop()

def print_test(x):
  print(x)
  
