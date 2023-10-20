# Assignment #1
### Part I
Digital input project
![Idea1_Yujia Li](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/ffb9a32a-0c2c-4d66-b0b0-73c95ed00563)
![Idea2_Yujia Li](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/90959475-ebd5-4161-9f92-2b02c653a086)

### Part II
#### Project Description
I have decided to go with the second idea, "glove controller." My initial concept is to use this project as the hardware interaction part of a UI/UX project. It would involve controlling specific items or on-screen content through finger interactions. For example, using finger taps to switch drawing tools or possibly incorporating angle sensors or pressure sensors in future assignments to adjust certain attributes  (e.g., thickness, size, texture) of on-screen contents (e.g., lines, material spheres, objects). I haven't fully developed the entire project yet, but the current task is to first implement the finger interactions.
#### Interactive Behavior 01
Except for the thumb, each of the other four fingers has a corresponding RGB light. Whenever the thumb touches one of the fingers, the corresponding RGB light will be turned on. Even if the two fingers separate, the RGB light will remain on. The RGB light that is currently on will turn off only when the thumb touches another finger, and the RGB light corresponding to the newly touched finger will be turned on. If the thumb touches multiple fingers, all RGB lights will be turned off.
<img width="3732" alt="Flow Chart_Yujia Li" src="https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/ce769ff3-df1f-4c0d-a307-aa10ad4cbfd3">
### Part III
#### Flowchart Updates
<img width="3876" alt="Flowchart_v2" src="https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/7396990f-4742-4953-a456-4583b6328705">
#### Prototype Description
The glove controller has three states: "DEFAULT," "TAP," and "DOUBLE_TAP." In the "DEFAULT" state, the RGB light is black, and it checks if two fingers are touched each other. If they are, the RGB light turns green, and the current state becomes "TAP." In the "TAP" state, it checks if two fingers are touched each other for the first time. If they are, this closure will be recorded. If it's not the first closure and the time interval between the two closures is more than 300ms and less than 700ms, the RGB light turns blue, and the current state becomes "DOUBLE_TAP." In the "DOUBLE_TAP" state, it checks if the fingers are touched each other and if the time elapsed since the last contact is more than 500ms. If both conditions are met, the RGB light turns green, and the current state becomes "TAP."
#### Process Documentary
![IMG_1951](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/2d426845-6cc4-4422-a6ac-67d837862a86)
![IMG_1954](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/911f4311-bda9-477f-add6-4915bf4a90f5)
![IMG_1953](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/8c71294d-d3d2-4358-a649-8ab46b66d310)
![IMG_1952](https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/25553fb8-37b8-4f5f-9ab4-576d6fdb05c2)

https://github.com/Hazelilili/IXD-256-Advanced_Interactive_Prototyping/assets/48962522/9de71248-3ee0-4d4a-9fdd-cf22bee3ea20

