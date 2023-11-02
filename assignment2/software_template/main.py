import js as p5
from js import document

# Define a class for the falling circles
class FallingCircle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.speed = p5.random(1, 5)

    def fall(self):
        # Move the circle down
        self.y = self.y + self.speed
        if self.y > p5.height:
            self.y = 0
            self.x = p5.random(p5.width)
            self.speed = p5.random(1, 5)

    def display(self):
        # Draw the circle
        p5.fill(p5.color(0, 160, 251))
        p5.noStroke()
        p5.ellipse(self.x, self.y, self.r, self.r)

# Initialize the variables
data_string = None
data_list = None
light_val = None
angle_val = None
falling_circles = []

# load image data and assign it to variable:
plant_img = p5.loadImage('plant.png')

def setup():
    p5.createCanvas(300, 300)
    # change mode to draw images from center:
    p5.imageMode(p5.CENTER)

def draw():
    global data_string, data_list
    global light_val, angle_val
    global falling_circles

    # assign content of "data" div on index.html page to variable:
    data_string = document.getElementById("data").innerText
    # split data_string by comma, making a list:
    data_list = data_string.split(',')
    # assign 1st item of data_list to light_val:
    light_val = int(data_list[0])
    # assign 2nd item of data_list to angle_val:
    angle_val = int(data_list[1])

    # Draw the background
    # Change color based on the light_val
    p5.background(light_val, light_val, light_val) 

    # Draw the image
    img_width = p5.width
    img_height = p5.width * (plant_img.height / plant_img.width)
    p5.image(plant_img, p5.width / 2, p5.height / 2, img_width, img_height)

    # Update and display circles
    for circle in falling_circles:
        circle.fall()
        circle.display()

    # Adjust the number of circles based on the angle_val
    target_circle_count = p5.map(angle_val, 0, 255, 0, 50)
    
    # Add circles if there are less than the target
    while len(falling_circles) < target_circle_count:
        r = p5.random(5, 25)
        new_circle = FallingCircle(p5.random(p5.width), -r, r)
        falling_circles.append(new_circle)

    # Remove circles if there are more than the target
    while len(falling_circles) > target_circle_count:
        falling_circles.pop()

    for circle in falling_circles:
        circle.fall()
        circle.display()

    # Remove circles that have fallen off the screen
    still_on_canvas = []

    for circle in falling_circles:
        # Check if the circle is still within the canvas
        if circle.y < p5.height:
            # If the circle is still within the canvas, add it to a new list
            still_on_canvas.append(circle)

    # Update the falling_circles list
    # keep only the circles that are still within the canvas
    falling_circles = still_on_canvas
