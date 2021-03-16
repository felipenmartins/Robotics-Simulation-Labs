# Lab 2 – Line-following State-Machine

## Objectives
The goal of this lab is to learn more about controllers in Webots, and to implement a line-following behavior in Python, based on a state-machine. 

## The e-puck robot
Webots contains a realistic model of e-puck, a small differential drive mobile robot. The movement of this type of robot is controlled by adjusting the speed of each wheel. The robot also has several sensors. 

To detect obstacles, e-puck contains 8 infra-red distance sensors around its body. Other 3 infra-red sensors are mounted under its base, pointing to the floor, which enables the implementation of a line-following behavior. 

## Tasks
You are going to load an example world that shows a line-follower behavior implemented with a state machine. First, you will be able to play with a simple graphical programming interface to understand and modify the state machine. Then, you will built a line-following behavior in Python.

1. Click on “Open Sample Worlds” and go to robots `gctronic > e-puck` and select `e-puck_botstudio_with_floor_sensors.wbt`. You should see a world as shown in Figure 1.

![Webots screenshot with e-puck](/Lab2/Webots_screenshot_with_e-puck.png)
Figure 1. Webots screenshot with the world “e-puck_botstudio_with_floor_sensors.wbt”.

2. Double-click on the e-puck robot: a new window shows the BotStudio, which is a graphical interface to build simple programs for the e-puck robot (see Figure 2). The BotStudio shows a line-follower behavior implemented in the form of a state-machine.

![BotStudio screenshot](/Lab2/BotStudio.png)
Figure 2. BotStudio screenshot with the line-follower state-machine (left) and values of e-puck sensors and motor speeds (right).

3. Start the simulation on the Webots screen by clicking the “play” button in the top menu. The robot will not move. To start the robot controller, you must click on the black upward pointing arrow in the BotStudio screen (Figure 2). 

4. Observe the behavior of the robot in the simulation. At the same time, observe the BotStudio window. Note the transitions between states and the measurements indicated by the sensors on the e-puck viewer (on the right side of the BotStudio window). The e-puck viewer shows the values returned by each of the robot sensors while the simulation is running. 

5. Now, click again on the upward pointing arrow in the BotStudio screen to stop the robot.

6. In the BotStudio window, click on the states “forward”, “turn left” and “turn right” and observe the e-puck viewer. Do the same for the conditions for transition between states. 

7. Play a bit with the values of motor speeds and sensors to understand their effect in the behavior of the robot. 

8. Modify the values of motor speed and sensors to make the robot follow the line as fast as possible, without missing it. 

9. Follow [Webots Tutorial 4](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?tab-language=python) to better understand the e-puck model and how to control it.

10. Finally, implement the line-follower behavior in Python using what you learned from Tutorial 4. Create a new controller in Python and write a program that implements the same state-machine shown in the BotStudio example. You can use the parameters that you think are best. 

## Conclusion
After following this lab you should know more about the e-puck robot model, how to program a controller for it in Python, and how to program a robot behavior based on state-machine. 

## Challenge
Add obstacles to the world and try to change the state-machine to make e-puck avoid obstacles placed on its way.

## Solution
Try to implement the state-machine code yourself before checking the solution! After a successfull implementation, or if you need inspiration, an example code is available [here](/Lab2/line_following_behavior.py).

The video below shows the solution code in action:
[![Video screenshot](/Lab2/line-follower_video_screenshot.png)](https://youtu.be/nW06dLEe-AU).
