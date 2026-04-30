# Lab 3 – Vision-based Line-following Behavior

## Objectives
In this lab you will implement another line-following behavior, but now using images from the robot's camera as input, instead of its ground sensors. The goal is to understand the basic steps to process images and acquire relevant information to control the robot.

## Pre-requisites
* You must have Webots R2022a (or newer) properly configured to work with Python. 
* You must know how to create a robot controller in Python and how to run a simulation. 
* You should have a working solution of [Lab 2](../Lab2/ReadMe.md).  

If you are still missing any of those, please go back to previous labs and complete the corresponding tasks.

## The e-puck robot camera
The [e-puck model in Webots](https://www.cyberbotics.com/doc/guide/epuck?version=R2021a) contains a camera that generates images from the environment that can be processed and used in our code. It is a color camera with a maximum resolution of 640x480 pixels.

Figure 1 shows a screenshot of the e-puck robot following a line using a vision-based controller. The pink lines in front of the robot indicate the view frustum (the camera's field of view - what objects are visible). The two windows next to the robot show: 

1. The _Camera View_ window shows the environment as seen by the robot's camera. On top of the original image, we are drawing the Region-of-Interest - **ROI** (green box), the center of the image (blue line) and the desired position of the robot (red dot).
2. The _Binary_ window shows a processed version of the same image, emphasizing its verical edges.

In this lab, you will understand how this is done and how to use it to control the robot. 

![Webots screenshot with e-puck and camera images](../Lab3/vision_controller_screenshot.png)
###### Figure 1. Webots screenshot with the e-puck robot following the line using a vision-based controller. 


------------ Estou aqui ----------------


## Image Processing



![Webots screenshot with e-puck and camera images](../Lab3/vision-based_flowchart.png)
###### Figure 2. Flowchart of the vision-based line-following controller. 






## Tasks

bla bla bla




## Solution
Try to implement the code yourself before checking the solution! An implementation is available [here](../Lab3/line_following_with_camera.py).

## Challenge: ????

bla bla bla



------------ Daqui pra frente está pronto. ------

## Conclusion
After completing this lab you have a better understanding of how to process images from a camera to obtain information for robot navigation.

## Next Lab
In the next lab we will use encoder values to estimate the position and orientation of the robot while it navigates. 

Go to [Lab 4](../Lab4/ReadMe.md) - Odometry-based Localization

Back to [main page](../README.md).
