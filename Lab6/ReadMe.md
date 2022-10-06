# Lab 6 - Combine Behaviors to Execute a Mission

## Update note
**The description of this lab was written based on older Webots versions (prior to R2022a). If you are using Webots R2022a or newer, please note that Webots changed its global coordinate system! It now uses ENU by default - [see detailed information here](https://cyberbotics.com/doc/blog/Webots-2022-a-release). Because of that, the world available on the ZIP file will not load propely. I intend to update this file in the future.**

## Objectives
The main goal of this lab is to combine different behaviors to make your robot execute a complex mission. You will also investigate and choose a robot to perform the mission, based on its features.

## Pre-requisites
* You must have Webots **R2021b (or older)** properly configured to work with Python (see [Lab 1](../Lab1/ReadMe.md)).
* You must know how to create a robot controller in Python and how to run a simulation (see [Lab 1](../Lab1/ReadMe.md)). 
* Download the file [wall_following_with_obstacles.zip](../Lab6/wall_following_with_obstacles.zip) and unzip it in a folder of your preference. After unzipping the file, open the world `...\wall_following_with_obstacles\worlds\wall_following_with_obstacles.wbt`. You should see a Pioneer 3-DX robot at the start position, as shown in Figure 1.

![screenshot_starting_position.png](../Lab6/screenshot_starting_position.png)
###### Figure 1. Screenshot showing the Pioneer 3-DX robot at the starting position of the world.

_Note: the configuration of the central wall changes every time you load or reset the world._

The provided world is based on a sample world from Webots, called _wall_following_. The main difference is that the provided world is populated with obstacles, as shown in Figure 2. The original sample world is available at `robotbenchmark -> wall_following -> wall_following.wbt`.

![screenshot_pioneer.png](../Lab6/screenshot_pioneer.png)
###### Figure 2. Some obstacles included in the provided world.

## Tasks
Follow the steps below to successfuly complete this lab.

1. **Read the description of the behaviors and the mission**. 

2. **Familiarize yourself with the provided environment**.

3. **Choose a wheeled mobile robot** to use in this lab from  [this list](https://cyberbotics.com/doc/guide/robots). Think about the requirements of the mission and the features of the robot! Investigate the characteristics of the robot: its type, available sensors, actuators, maximum speed, etc. You are free to add extra sensors to the robot of your choice.

4. **Investigate the functions used in Python to control the robot and how the robot XYZ reference frame is oriented with respect to the world**. In the [robot list](https://cyberbotics.com/doc/guide/robots) you can click on each robot to find specific information about it.

5. **Implement the behaviors in Python**: task controllers wall-following, trajectory tracking and obstacle avoidance, according to the description below. 

6. **Implement a finite-state machine to implement the mission** described below (also in Python).

### Description on the behaviors
1.	**Wall-following**: build a program so that the robot successfully follows the central wall while keeping it on its right side. In other words, the robot should follow the central wall in the opposite direction from the example program provided in the world. You can use the provided example as a base for your program, but you might need to adapt it to your robot and adjust the PID gains. The example program with a wall-following behavior can be found in the folder `...\wall_following_with_obstacles\controllers`.

2.	**Trajectory tracking**: implement the trajectory tracking controller as described in Lab 4. The controller must include the saturation terms to avoid the generation of very high reference speeds when the error is too big. The maximum reference speeds must be equal to or lower than the maximum speeds achieved by the robot.

3.	**Obstacle avoidance**: develop and implement an obstacle avoidance behavior so that the robot avoids obstacles. Your robot must avoid obstacles without touching them. 

### Description of the mission
- The initial position of the robot is (0, 0) m. 
- The robot must move straight towards the central wall until its distance to it is 0.5m.
- Then, the robot must follow the wall while keeping it on its right side until it gets to position (??, 20.0) m. 
- After getting to the above position, the robot must make a full turn around its own center (360 degrees).
- Then, it should execute trajectory tracking + obstacle avoidance behaviors to go back to its original position. 

## Solution
No solution is provided for this lab.

## Conclusion
After completing this lab you are able to combine many behaviors for a mobile robot to execute a complex mission. Keep in mind that this is a challenging exercise! 

## Next Lab (bonus)
Go to [Lab 7](../Lab7/README.md) - Robot Soccer Challenge

Back to [main page](../README.md).
