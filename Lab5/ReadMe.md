# Lab 5 - Combine Behaviors to Complete a Mission

## Objectives
The main goal of this lab is to combine different behaviors to make your robot perform a complex mission. You will implement a state machine and simple behaviors (like wall-following, go-to-goal with PID etc.) for the robot to navigate through a maze while tracking its pose.

## Pre-requisites
* You must have Webots R2023a (or newer) properly configured to work with Python (see [Lab 1](../Lab1/ReadMe.md)).
* You must know how to create a robot controller in Python and how to run a simulation (see [Lab 1](../Lab1/ReadMe.md)). 
* You must know how to [implement simple behaviors](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/robot_behaviors.ipynb), a [state machine](../Lab2/ReadMe.md), a [localization algorithm](../Lab3/ReadMe.md) and a controller for robot navigation (either [PID](../Lab4/ReadMe.md) or [trajectory tracking](../Lab5/ReadMe.md)). 
* Download the file [webots-maze.zip](../Lab5/webots-maze.zip) and unzip it in a folder of your preference. After unzipping the file, open the world `...\webots-maze\worlds\e-puck_maze.wbt`. You should see an environment similar to the one shown in Figure 1.

![webots_maze.png](../Lab5/webots_maze.png)
###### Figure 1. Screenshot showing the maze environment. The e-puck robot starts at the center of the checker texture square (right) and must navigate to the red tunnel (left).

## Description of the Mission
**The mission of your robot is to pass under the red tunnel**. The e-puck robot starts at the center of the checker texture square (right) and must navigate through the maze to get to the red tunnel (left). The robot can follow any free path (it does not need to be the shortest nor the fastest).

### Minimum Requirements
There are many ways to implement a program for the robot to complete this mission. But, since the goal of this assignment is to practice concepts from previous labs, you **must** implement at least the following functions:

- localization algorithm;
- go-to-goal controller with PID _or_ trajectory tracking controller;
- wall-following _or_ corridor-following behavior;
- state machine to select behaviors.

The controllers and behaviors **must** generate reference values for **linear and angular velocities**.

The environment **cannot** be changed: no object can be added, moved or removed from the provided world.

Figure 2 illustrates the e-puck robot navigating through the maze by switching between three different behaviors: wall-following, curve +90 degrees and turn -90 degrees. The selection of the active behavior is done by a state machine that uses the proximity sensor readings for transitions between states. A bare-bones code for this is provided in the ZIP file, and can be used as a template for the implementation of your solution.

![e-puck_maze_following.gif](../Lab5/e-puck_maze_following.gif)
###### Figure 2. Maze navigation by switching between three simple behaviors: wall-following, curve +90 degrees and turn -90 degrees.


## Solution
No solution is provided for this lab. Explanation on how to implement simple behaviors (like wall-following) is provided in the Jupyter Notebook about [Behaviors for Mobile Robot Control](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/robot_behaviors.ipynb).

## Conclusion
After completing this lab you are able to combine many behaviors for a mobile robot to execute a complex mission. 

## Next Lab
Go to [Lab 6](../Lab6/README.md) - Trajectory Tracking Controller

Back to [main page](../README.md).
