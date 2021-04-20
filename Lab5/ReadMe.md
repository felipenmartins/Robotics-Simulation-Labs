# Lab 5 - Combine Behaviors to Execute a Task

## Objectives
The goal of this lab is to combine different behaviors to make your robot execute a complex task. You will also investigate and learn about another mobile robot widely used in research: the Pionneer 3 DX.

## Tasks
Your group must make use of the robotics simulator Webots to implement the Robotics Task. The software is freely available at: https://cyberbotics.com/#cyberbotics

You must use the sample world called “wall_following”. To open this world in Webots, click on File -> Open Sample World -> samples -> robotbenchmark -> wall_following -> wall_following.wbt
The world and the corresponding robot are loaded. They are illustrated in Figure 1. 

 
Figure 1. Environment and robot to be used in the project.

Two important things to note are: 
-	the configuration of the central wall changes every time you load or reset the world;
-	the orientation of the XYZ robot reference frame is different from what we are used to. 

What does your group have to do?

- Investigate the characteristics of the robot: its type, available sensors, actuators, maximum speed, etc. Investigate the functions used in Python to control the robot and how the robot XYZ reference frame is oriented with respect to the world.
- Implement 3 behaviors (task controllers) in Python: wall-following, trajectory tracking and obstacle avoidance. 
- Implement a finite state machine (also in Python) to control the execution of the mission described below.

Description on the behaviors: 
1.	Wall-following: adjust the example program so that the robot successfully follows the wall, while keeping it on its right side. In other words, the robot should follow the central wall in the opposite direction from the example program. You might need to adjust the PID gains.
2.	Trajectory tracking: implement the trajectory tracking controller as described in the robotics lessons. The controller must include the saturation terms to avoid the generation of very high reference speeds when the error is too big. The maximum reference speeds must be equal or lower than the maximum speeds achieved by the robot.
3.	Obstacle avoidance: develop and implement an obstacle avoidance behavior so that the robot avoids obstacles without touching them. 

Description of the mission:
a)	The initial position of the robot is (0, 0) m. 
b)	The robot must move straight towards the central wall until its distance to it is 0.5m.
c)	Then, the robot must follow the wall while keeping it on its right side until it gets to position (??, 20.0) m. Figure 2 illustrates the desired position of the robot at this point.
d)	After getting to the above position, the robot must make a full turn around its own center (360 degrees).
e)	Then, it should execute trajectory tracking + obstacle avoidance behaviors to go back to its original position. 

 
Figure 2. Desired position of the robot after following the wall.

## Main Page
Back to [main page](../README.md).
