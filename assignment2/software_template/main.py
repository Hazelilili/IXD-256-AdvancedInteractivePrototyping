import js as p5
from js import document

# 这些是您的全局变量
data_string = None
data_list = None

light_val = None
angle_val = None
png_image = None  # 用于加载和显示png图像

def preload():
    global png_image
    png_image = p5.loadImage('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&q=60&w=800&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGxhbnR8ZW58MHx8MHx8fDA%3D')  # 请替换为您的png图像的路径

def setup():
    p5.createCanvas(300, 300)
    p5.angleMode(p5.DEGREES)

def draw():
    global data_string, data_list
    global light_val, angle_val
    
    # 从HTML元素获取数据
    data_string = document.getElementById("data").innerText
    data_list = data_string.split(',')
    
    if len(data_list) >= 2:
        light_val = int(data_list[0])
        angle_val = int(data_list[1])
    
    # 背景渐变
    for y in range(300):
        grad_color = p5.lerpColor(p5.color(0, 0, 0), p5.color(255, 255, 255), y/300 * (light_val/255))
        p5.stroke(grad_color)
        p5.line(0, y, 300, y)
    
    # 绘制png图像
    p5.image(png_image, 0, 0, p5.width, p5.height)
    
    # 根据angle_val绘制下落的圆
    num_circles = p5.map(angle_val, 0, 255, 0, 50)  # 您可以根据需要调整这里的范围
    p5.fill(p5.color(0, 0, 255))
    p5.noStroke()
    
    for _ in range(int(num_circles)):
        x = p5.random(0, 300)
        y = p5.random(250, 300)
        r = p5.random(5, 25)
        p5.ellipse(x, y, r, r)

# 剩下的代码应当是与您的硬件设备进行交互以获取sensor数据的部分


