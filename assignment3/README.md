# Assignment3
### Part I
Idea Sketch
![Rube Goldberg Machine Idea_Yujia](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/9e85e0c7-97b2-4954-b943-ae9c6cdabb31)
Flowchart
![Rube Goldberg Machine Flowchart_Yujia](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/ac161e8e-cb60-4573-ac5b-13fb1e22756b)

### Part II
#### Project Description
I have decided to go with the second idea, "Virtual Plant." This project will use two sensors — a light sensor and a potentiometer — to control graphics on the screen. I plan to use the potentiometer to adjust the number of blue circles, which will simulate water drops, and the light sensor to control the color gradient of the background, which will simulate sunlight. The whole idea will be:
- As the value read from the potentiometer changes, vertically falling water droplets appear on the screen, and the number of droplets changes in response to the value.
- As the value from the light sensor changes, the background color changes in a linear gradient between black and white. At brightest environment, the background is white, and at darkest, the background is black.
- (Optional) Adding the built-in button of the Atom 3 Lite as the third input, each press will cause the plant to lose a petal. However, depending on the values and effects from the other two inputs, whenever the screen simultaneously meets three conditions: 1. At least ten water droplets, 2. 50% brightness, and 3. maintained for one minute, the plant will regrow a petal.

However, due to time constraints, limitations of the tools, and personal capability considerations, the linear gradient and the optional were eventually removed. The plants, which were originally planned to be drawn using code, were replaced with a PNG.

In the process of working on this project, I encountered a variety of problems, such as the two sensors not working simultaneously and the angle sensor's readings spiking to 255 along with the light sensor, and so on. In the end, issues were resolved.

#### Process Documentary
##### Process

