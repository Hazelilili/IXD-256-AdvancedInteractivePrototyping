import js as p5
from js import document

data_string = None
data_list = None
light_val = None
angle_val = None
falling_circles = []

# Load the image data and assign it to a variable
plant_img = p5.loadImage('plant.png')

def setup():
    p5.createCanvas(300, 300)
    p5.imageMode(p5.CENTER)

def draw_background_gradient():
    global light_val
    p5.noStroke()

    # Image drawing
    img_width = p5.width
    img_height = p5.width * (plant_img.height / plant_img.width)  # maintain original aspect ratio
    p5.image(plant_img, p5.width / 2, p5.height / 2, img_width, img_height)

   

def draw():
    global data_string, data_list
    global light_val, angle_val
    global falling_circles

    # Draw background gradient based on light sensor value
    draw_background_gradient()

    # Parse sensor data
    data_string = document.getElementById("data").innerText
    data_list = data_string.split(',')
    light_val = int(data_list[0])
    angle_val = int(data_list[1])

    # Falling circles based on angle sensor
    num_new_circles = p5.map(angle_val, 0, 255, 0, 5)
    for _ in range(int(num_new_circles)):
        falling_circles.append({
            "x": p5.random(0, 300),
            "y": -10,  # starts a bit outside of canvas
            "r": p5.random(5, 25),
            "speed": p5.random(1, 3)
        })

    p5.fill(0, 0, 255)
    p5.noStroke()
    for circle in falling_circles:
        p5.ellipse(circle["x"], circle["y"], circle["r"], circle["r"])
        circle["y"] += circle["speed"]
    
   
