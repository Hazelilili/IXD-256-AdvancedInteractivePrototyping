import js as p5
from js import document

data_string = None
data_list = None

light_val = None
angle_val = None


def setup():
    p5.createCanvas(300, 300)
    p5.angleMode(p5.DEGREES)
    p5.rectMode(p5.CENTER)
    p5.strokeCap(p5.SQUARE)

def draw_flower(x, y, scale, rotation, color):
    p5.push()
    p5.translate(x, y)
    p5.rotate(rotation)
    p5.fill(color)
    p5.noStroke()
    
    # Circle at the center
    p5.ellipse(0, 0, 20 * scale, 20 * scale)
    
    # Traps around the center
    for i in range(6):
        p5.push()
        p5.rotate(60 * i)
        p5.beginShape()
        p5.vertex(0, 0)
        p5.vertex(30 * scale, -15 * scale)
        p5.vertex(60 * scale, 0)
        p5.vertex(30 * scale, 15 * scale)
        p5.endShape(p5.CLOSE)
        p5.pop()
    
    p5.pop()

def draw():
    global data_string, data_list
    global light_val, angle_val
    
    data_string = document.getElementById("data").innerText
    data_list = data_string.split(',')
    light_val = int(data_list[0])
    angle_val = int(data_list[0])

    # Background gradient
    grad_color = p5.map(light_val, 0, 255, 0, 100)
    p5.background(p5.lerpColor(p5.color(0, 0, 0), p5.color(255, 255, 255), grad_color/100))
    
    # Draw the stem
    p5.strokeWeight(5)
    p5.stroke(p5.color("#F2F2F2"))
    p5.line(150, 150, 150, 300)
    
    # Draw the flower layers
    draw_flower(150, 150, 1.2, 30, p5.color("#C2FFCC"))
    draw_flower(150, 150, 1.2, -30, p5.color("#3FF05B"))
    draw_flower(150, 150, 1, 0, p5.color("#0DA926"))
    
    # Draw falling circles
    num_circles = p5.map(angle_val, 0, 255, 0, 30)
    p5.fill(p5.color(0, 0, 255))
    p5.noStroke()
    
    for _ in range(int(num_circles)):
        x = p5.random(0, 300)
        y = p5.random(150, 300)
        r = p5.random(5, 25)
        p5.ellipse(x, y, r, r)

