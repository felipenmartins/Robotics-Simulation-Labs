# Lab 9 – Path planning with Dijkstra

## Objective
Robot path planning finds a sequence of valid destinations (intermediate goals) to move a robot from a start point to a destination in a known environment. The goal of this lab is to apply Dijkstra's algorithm to plan a path and then use the go-to-goal behavior for the e-puck robot to follow it. 

<center>
<img src="../Lab9/planned_path_2.png" alt="Map and planned path" width="350"/>
</center>

###### Figure 1. Plot of a map of the environment: the map is divided into cells (grid map); black lines represent all possible paths for the robot; numbers represent the cost for the robot to cross the corresponding cell; red line shows the planned path that results in lower cost from start (0, 0) to goal (12, 16). 

## Dijkstra's Algorithm

Dijkstra's Algorithm is a graph-based path finding algorithm that **guarantees the optimal path** in a weighted graph. Such optimal path is obtained by finding the path of minimal _cost_, which can be related to different aspects, like distance, battery usage, time etc.. In the context of robotics, Dijkstra's Algorithm  is particularly useful for path planning in known environments (known map). 

In this lab, we are going to work with a **grid map**, which is a way to represent the environment as a grid of small cells, as illustrated in Figure 1. Such map represents a **graph** where each **node** corresponds to a position (a grid cell), and **edges** represent connections between cells. The **weights** represent the cost of moving from one node to another (the numbers in Figure 1, which are costs associated to the robot arriving at each cell). Dijkstra's algorithm always finds the **least-cost path from a start node to a goal node**, if it exists. Such a path is also the shortest if the costs are proportional to the distances between nodes. However, if the costs represent other aspects (like presence of obstacles, for example), then the resulting path might not be the shortest, as illustrated by Figure 1. 

A more detailed explanation can be found in the Jupyter Notebook on [Dijkstra's Algorithm for Robotic Path Planning](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/path_planning_dijkstra.ipynb). There, you will find an explanation on how Dijkstra's Algorithm work and how to implement it in Python. The notebook also shows how to define a grid environment for the robot and how you can visualize the map and generated path using plots.


## Pre-requisites
* You must have Webots R2023a (or newer) properly configured to work with Python (see [Lab 1](../Lab1/ReadMe.md)).
* You must know how to create a robot controller in Python and how to run a simulation (see [Lab 1](../Lab1/ReadMe.md)). 
* You must know how to [implement simple behaviors](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/robot_behaviors.ipynb), and a [state machine](../Lab2/ReadMe.md) to select the robot behavior. 

## Tasks

We will start with a line-following algorithm on the same world provided in the ZIP file of Lab 8 (see above). Contrary to Lab 8, we are not going to use an external microcontroller in this lab. 

Follow the steps below to prepare your environment:

1. If you haven't done so, go back to [Lab 8](../Lab8/ReadMe.md) and follow steps 1-3 to install the world shown in Figure 1. 

2. After that, **create a new Python controller** for the robot, and **copy the code** from [`line_following_behavior.py`](../Lab2/line_following_behavior.py) to it. **Save the controller** file (use the save button on top of the code).

3. **Run the Webots simulation** and verify that the robot follows the line. 

This example implements a simple line-following behavior state machine, like the one from Lab 2. It is expected that the robot will drift off the line at corners. 

_Tip:_ Change the code to force the wheels speeds to be always zero. Then, while running the simulation, move the robot manually over the line to check the message and state printed in the console.


You need to complete two tasks in this lab:


-
- Incorporate go-to-goal controller to follow the planned path
-
-



## Solution
No solution is provided for this lab.

## Challenge
Using the example provided in [Lab 8](../Lab8/ReadMe.md), program Dijkstra's Algorithm **in the microcontroller** using MicroPython and make the robot navigate the planned path between arbritary nodes in the field. 

**Important!** NumPy does not work in MicroPython. To use a 2D array in MicroPython, you can create a list of lists, where each inner list represents a row. For example, you can define a 2D array like this: 

```array = [[0 for _ in range(columns)] for _ in range(rows)]```

_Rows_ and _columns_ are the desired dimensions of the array. To access elements, use two indices: 

```value = array[1][2]  # Gets the element in the 2nd row and 3rd column```


## Conclusion
After following this lab you should know how to use Dijkstra's algorithm to plan optimal paths in known environments. By completing the challenge, you also practice how to implement the algorithm in the microcorntoller.


## Next Lab
Program robots to play soccer as a team in the next lab!

Go to [BONUS](../SoccerSim/ReadMe.md) - Robot Soccer Challenge

Back to [main page](../README.md).
