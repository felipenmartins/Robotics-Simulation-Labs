# Lab 3 – Odometry-based Localization

## Objective
The goal of this lab is to implement a simple algorithm for odometry-based robot localization and evaluate its accuracy.

## Robot Pose
To see the pose of the robot as calculated by Webots, click on “DEF E_PUCK E-puck” on the left menu and select “translation”. You will see the values of position and orientation of the robot (see Figure 1). You should print the position calculated by your functions at the end of each cycle, as shown in Figure 1, to facilitate comparison with the pose as calculated by Webots.

![Robot pose in Webots](../Lab3/Webots_robot_pose.png)

Figure 1. Webots screenshot showing robot pose calculated by the simulator (left) and by the Python code (bottom).

## Pre-requisites
* You must have Webots R2022a (or newer) properly configured to work with Python (see [Lab 1](../Lab1/ReadMe.md)).
* You must know how to create a robot controller in Python and how to run a simulation (see [Lab 1](../Lab1/ReadMe.md)). 
* You should have a working solution of [Lab 2](../Lab2/ReadMe.md). If not, please use the provided solution. 

### Update note
_The description of this lab, the template and solution code were updated on 03-03-2022 to make them compatible with the new global coordinate system adopted as default by Webots R2022a (or newer). If you are using an older version of Webots, please make sure your code is adapted accordingly [(see more details at the end of this page).](#a-note-on-webots-reference-frame)_

## Tasks
Your main task is to write code to implement the functions below to add localization capability to your line-following behavior. The functions below should be called in sequence in the main loop of your program:
```
    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)
    
    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, R, D)
    
    # Compute new robot pose
    [x, y, phi] = get_robot_pose(u, w, x, y, phi, delta_t)
```

The tasks are listed below:

1. Write the function `get_wheels_speed(encoderValues, oldEncoderValues, delta_t)` to calculate the speed of the robot wheels based on encoder readings. Test your code before moving to the next step.
2. Write the function `get_robot_speeds(wl, wr, R, D)` to calculate the linear and angular speeds of the robot based on the speed of its wheels. Test your code before moving to the next step.
3. Write the function `get_robot_pose(u, w, x, y, phi, delta_t)` to calculate the position and orientation of the robot based on its orientation and linear and angular speeds.
4. Compare the pose calculated by your functions with the pose calculated by Webots in different moments of the simulation. 

### Think about the following questions

* How accurate is the odometry-based localization?
* In what conditions is odometry-based localication useful? And when is it problematic?

### Some information for implementing the code
The definition of the variables used in the functions is given below.

```
Robot pose and speed in (x,y) coordinates:
x = position in x [m]
y = position in y [m]
phi = orientation [rad]
dx = speed in x [m/s]
dy = speed in y [m/s]
dphi = orientation speed [rad/s]

Robot wheel speeds:
wl = angular speed of the left wheel [rad/s]
wr = angular speed of the right wheel [rad/s]

Robot linear and angular speeds:
u = linear speed [m/s]
w = angular speed [rad/s]

Period of the cycle:
delta_t = time step [s]
```

To calculate robot localization you will need to use some physical parameters of the robot:

```
R = radius of the wheels [m]: 20.5mm 
D = distance between the wheels [m]: 52mm 
```

You can use the pieces of code below to initialize the encoder sensors and to read encoder values in the main loop of your program:

To initialize encoders:
```
encoder = []
encoderNames = ['left wheel sensor', 'right wheel sensor']
for i in range(2):
    encoder.append(robot.getDevice(encoderNames[i]))
    encoder[i].enable(timestep)
```

To read the encoders in the main loop:
```
    encoderValues = []
    for i in range(2):
        encoderValues.append(encoder[i].getValue())    # [rad]
```
The encoder values are incremented when the corresponding wheel moves forwards and decremented when it moves backwards.

I recommend you try to modify your line following code from Lab 2 to implement the localization as described above. Try doing it yourself, first. If your code is not working, or you need inspiration, you can use the [provided template](../Lab3/lab3_template.py). 

## Conclusion
After following this lab you should know more about the implementation and limitations of odometry-based localization for mobile robots.

## Challenge: Go-to-goal behavior with PID
Modify the line-following state-machine to create a new state that implements a "go-to-goal" behavior using a PID controller. This state should be activated when the robot reaches approximately half of the track. In other words, the robot starts by following the line using the state-machine with localization implemented in this lab. When it gets half-way through the path, the "go-to-goal" state is activated. A list of goal positions is given in the program. One should be able to add as many goal positions as desired. After reaching the final goal position, the robot must stop.

Implement your code so that the robot goes from its current position to the next goal position, stops, and stays there for some short time (1 second, for example). Then, the robot should move to the subsequent goal position and repeat the cycle until it reaches the final goal position. Everytime the robot stops at a goal, it ha to print its own position and error in x and y.

Demonstrate your code by making the robot go to the 4 corners of the field (without touching the walls), and then to the center of the field. For this challenge, there is no need to have obstacle avoidance working.

## Super challenge: 1-D Kalman Filter
Use another sensor (like a compass or gyroscope) to estimate the orientation of the robot. Implement a 1-D Kalman Filter to combine the values given by this extra sensor with the orientation calculated via odometry to get a better estimate of the robot orientation. In [this post](https://medium.com/analytics-vidhya/kalman-filters-a-step-by-step-implementation-guide-in-python-91e7e123b968) you find explanation about the Kalman Filter and how to implement it in Python. 

## Solution
Try to implement the localization code yourself before checking the solution! After a successfull implementation, or if you need more inspiration than the template, an example code is available [here](../Lab3/line_following_with_localization.py).

### A note on Webots Reference Frame
In Webots R2021b and older, the robot moves in the XZ plane! Figure 2 shows the orientation of the reference frames adopted in older versions of Webots (left) and the orientation of the reference used in the newer versions (right). If you are using a version of Webots older than R2022a, you need to adapt your code accordingly. Please, see the [Webots R2022a release notes](https://cyberbotics.com/doc/blog/Webots-2022-a-release) for more details.

![Webots Reference Frame](https://raw.githubusercontent.com/cyberbotics/webots/released/docs/blog/images/flu-enu.png) 

Figure 2. Orientation of the reference frames used in old (left) and new (right) Webots versions [(source)](https://cyberbotics.com/doc/blog/Webots-2022-a-release).

## Next Lab
Go to [Lab 4](../Lab4/ReadMe.md) - Trajectory Tracking Controller

Back to [main page](../README.md).
