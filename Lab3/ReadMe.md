# Lab 3 – Vision-based Line-following Behavior

## Objectives
In this lab you will implement another line-following behavior, but now using images from the robot's camera as input, instead of its ground sensors. The goal is to understand the basic steps to process images and to acquire relevant information to control the robot. You will also investigate how camera noise can influence the performance of the robot controller.

## Pre-requisites
* You must have Webots R2022a (or newer) properly configured to work with Python. 
* You must know how to create a robot controller in Python and how to run a simulation. 
* You must have a working solution of [Lab 2](../Lab2/ReadMe.md).  
* You must have a basic understanding of digital image representation and how to use some functions for image processing using Python and Open CV. If you need a refresh on this, please refer to the Jupyter Notebook on [Digital Image Processing](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/image_processing_example.ipynb).

If necessary, please go back to previous labs and complete the corresponding tasks.

## The e-puck robot camera
The [e-puck model in Webots](https://www.cyberbotics.com/doc/guide/epuck?version=R2021a) contains a camera that generates images from the environment that can be processed and used in our code. It is a color camera with a maximum resolution of 640x480 pixels.

Figure 1 shows a screenshot of the e-puck robot following a line using a vision-based controller. The pink lines in front of the robot indicate the view frustum (the camera's field of view - what objects are visible). The two windows next to the robot show: 

1. The _Camera View_ window shows the environment as seen by the robot's camera. On top of the original image, we are drawing the Region-of-Interest - **ROI** (green box), the horizontal center of the image (blue line) and the estimated center of the line on the floor (red dot).
2. The _Binary_ window shows a processed version of the same image, emphasizing its verical edges.

![Webots screenshot with e-puck and camera images](../Lab3/vision_controller_screenshot.png)
###### Figure 1. Webots screenshot with the e-puck robot following the line using a vision-based controller. 

In this lab, you will understand how this is done and how to use it to control the robot. The next section explains the image processing pipeline used in the available example code.

## Image Processing Pipeline
The image processing pipeline is illustrated in Figure 2, which reproduces the image shown by _Camera View_ window next to a flowchart of the example code [available here](../Lab3/line_following_with_camera.py). As explained above, the Region-of-Interest (ROI) is represented by the green box, the center of the image is indicated via the blue line and the center of the line on the floor is given by the red dot. Because the center of the camera view is aligned with the center of the robot, the objective of the controller is to change the robot's orientation so that the blue line aligns with the red dot. The idea is that the robot will follow the line when moving forwards as long as its orientation is continuously adjusted to align the center of the image with the center of the line. 

![Webots screenshot with e-puck and camera images](../Lab3/vision-based_flowchart.png)
###### Figure 2. Camera image and flowchart of the vision-based line-following controller. The image processing pipeline is illustrated by the blue blocks.

The flowchart in Figure 2 implements the classical see-think-act cycle for robot control. After the initialization of variables and definition of functions, the main loop executes in sequence:

* **See**: _Get image_ and _Get line offset_ blocks. 
* **Think**: _Calculate angular speed_, which calculates the speeds of each wheel based on the offset between the center of the image and the desired orientation of the robot.
* **Act**: _Set motor speeds_, which updates the motor speeds with the desired values.

The corresponding functions that implement the **think** and **act** parts in the [example code available here](../Lab3/line_following_with_camera.py) are quite simple. Please, check the code to understand them (the script is rich in comments to help with understanding).

From now on, we are going to focus on the functions in the **See** part of the cycle, which are the ones that implement the **image processing pipeline**.

The block _Get image_ refers to the function `webots_image_to_bgr(camera)`, which gets an image from the Webots simulated camera and convert it to OpenCV BGR format for further processing using OpenCV functions. 

Then, the block _Get line offset_ further processes the image in the function `detect_line_position(image)`, which calculates the offset of the robot with respect to the line. Such offset is proportional to the distance of the center of the image to the center of the line. 

In robotics, it is important that the **see-think-act** cycle is executed in as little time as possible. In our case, the image is the only source of information about the environment, so it is important that a new frame is processed per cycle. The first three steps of the function `detect_line_position(image)` have the objective of reducing computational demand related to image processing. 

The function `detect_line_position(image)` is composed by the following steps, represented by the blue blocks in the flowchart:

1. _Sub-sample image_: The original resolution of the image is 640 x 480 pixels. In this step, the image is resized to 320 x 240 pixels. This is common procedure to speed up processing when fine details of the image can be ignored. 
2. _ROI_: Define a Region of Interest - only the part of the image inside this region is processed, the rest can be ignored. In our case, we defined the ROI in a low part of the image where the line to be followed is expected to appear.
3. _Convert to grayscale_: The color image is converted to gray scale, which reduces the number of channels to be processed from three to one, further reducing computational demand.
4. _Gaussian blur_: This step filters the image by executing a convolution with unity mask of size 3 x 3. This is important for noise reduction. The bigger the mask, the more intense is the filter. However, increasing the mask also increases image blur, which might affect proper detection of the line. 
5. _Center of mass along x_: First, the image is inverted (255-blurred), then image moments are computed. Because the image is inverted, the line on the floor now appears white, while the rest of the floor turns to black. This means that the moment `m00` corresponds to count all pixels of the line inside the ROI, resulting in its area. Moment `m10` corresponds to the horizontal distribution of the pixels inside the ROI. Dividing `m10` by `m00` gives the center of mass of the ROI along the `x` axis.
6. _Line offset_: Finally, the line offset is calculated with respect to the image center. Considering that the robot must follow the line on the floor, the line offset is proportional to the orientation error of the robot.

The rest of the functions display the images on the screen at every cycle.


## Tasks
Using the same Webots world as in Lab 2, create a new robot controller called `line_following_with_camera`. Copy the [example code](../Lab3/line_following_with_camera.py) to your newly created controller and run the simulation. Pay attention to the behavior of the robot and the images from its camera. 

Now, observe that the example code has two different functions to process the image to obtain the line offset: `detect_line_position(image)` and `detect_line_position_2(image)`. Both serve the same purpose and have similarities. However, they are different. The explanation about the image processing pipeline given above refers to the function `detect_line_position(image)`. Analyse the code of the other function to understand the differences that exist between them. Change the code to call `detect_line_position_2(image)` and observe the behavior of the robot and the images from its camera. Is there notable difference in terms of performance of the line-following behavior?

### Noise Analysis 
By default, Webots models a perfect camera (no noise and no motion blur). Because the line is black and thick, the floor is white, and the path is smooth, there is sufficient contrast and smooth image change as the robot follows the line. So, in our case, the performance does not suffer much from motion blur. 

However, camera noise does have a strong influence in the quality of the captured image. Figure 3 illustrates how the image from the camera is compromised when the noise level is set to 0.5. The degradation in image quality can impact the performance of the system.

![Resulting image with camera noise](../Lab3/screenshot_camera_noise.png)
###### Figure 3. Resulting image when camera noise is set to 0.5. 


Now you are going to investigate how camera noise affects the performance of the two functions used in line-following controller example code: 

- Click the e-puck robot, select "camera_noise" and increase its value. 
- Run the code to check if the robot is still able to follow the line. If not, reduce its value. _Noise values do not have to be integer numbers._  
- Check how the image generated by the camera and the images processed by the code is affected by the changing values of noise. 
- Repeate the steps above to check the performance of both `detect_line_position(image)` and `detect_line_position_2(image)` functions. 
- What are the maximum values of camera noise that each of the functions can support? Can you explain why the values are different (or the same, whichever is the case)?

## Challenge
Set camera noise to a value above which the robot no longer follows the line. Make changes in the code to improve the performance of the line detection so that the robot is able to follow the line with higher values of noise. 

## Solution
No solution is available for the challenge. Tips:
- Think about what you need to change to improve noise reduction in the image. 
- Look at the images from the camera to check if the generated offset makes sense. Can you change something in the controller?
- Not necessarily the same changes will solve the problem in both `detect_line_position(image)` and `detect_line_position_2(image)` functions.

## Conclusion
After completing this lab, you should have a better understanding of how to process images to obtain information for robot navigation. 

The articles [[1](https://www.scitepress.org/PublishedPapers/2015/55439/55439.pdf)] and [[2](https://www.mdpi.com/1424-8220/17/10/2359)] describe practical applications of vision-based line-following controllers in real world environments. In [[1](https://www.scitepress.org/PublishedPapers/2015/55439/55439.pdf)] we describe a controller for a drone to follow "lines" of the environment, like crops, sidewalks and rivers. In [[2](https://www.mdpi.com/1424-8220/17/10/2359)] we show how to apply a vision system with a simple webcam to drive a car in regular roads with lane-markings (see section 3 for details on how the image is processed).

## References
[1] Brandão, Alexandre S., Felipe N. Martins, and Higor B. Soneguetti. "A vision-based line following strategy for an autonomous UAV." 2015 12th International Conference on Informatics in Control, Automation and Robotics (ICINCO). Vol. 2. Scitepress, 2015. Available at: [https://www.scitepress.org/PublishedPapers/2015/55439/55439.pdf](https://www.scitepress.org/PublishedPapers/2015/55439/55439.pdf)

[2] Vivacqua, Rafael, Raquel Vassallo, and Felipe Martins. "A low cost sensors approach for accurate vehicle localization and autonomous driving application." Sensors 17.10 (2017): 2359. Available at: [https://www.mdpi.com/1424-8220/17/10/2359](https://www.mdpi.com/1424-8220/17/10/2359)

## Next Lab
In the next lab we will use encoder values to estimate the position and orientation of the robot while it navigates. 

Go to [Lab 4](../Lab4/ReadMe.md) - Odometry-based Localization

Back to [main page](../README.md).
