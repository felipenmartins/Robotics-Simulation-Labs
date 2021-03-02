# Lab 3 – Odometry-based Localization

## Objective
The goal of this lab is to implement a simple algorithm for odometry-based robot localization and evaluate its accuracy.

## Robot Pose
To see the pose of the robot as calculated by Webots, click on “DEF E_PUCK E-puck” on the left menu and select “Position”. You will see the values of position and orientation of the robot (see Figure 1). You should print the position calculated by your functions at the end of each cycle, as shown in Figure 1, to facilitate comparison with the pose as calculated by Webots.

![Robot pose in Webots](/Lab3/Webots_robot_pose.png)

Figure 1. Webots screenshot showing robot pose calculated by the simulator (left) and by the Python code (bottom).

## Taks
Your main task is to write code to implement the functions below to add localization capability to your line-following behavior. In the main loop of your program, those functions should be called in a sequence:
```
    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)
    
    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, r, d)
    
    # Compute new robot pose
    [z, x, phi] = get_robot_pose(u, w, z, x, phi, delta_t)
```
I recommend you try to modify your line following code from Lab 2 to implement the localization as described above. Try doing it yourself, first. If your code is not working, or you need inspiration, you can use the [provided template](/Lab3/lab3_template.py). 

## Webots Reference Frame
In Webots, the robot moves in the XZ plane! Figure 2 shows the orientation of the reference frames adopted in most cases (on the left) and in Webots (on the right). 

![Webots Reference Frame](/Lab3/Reference_frame_convention.png) 

Figure 2. Orientation of the reference frames used to develop our controller equations (left) and adopted by Webots (right).

## Some extra information for implementing the code
The definition of the variables used in the functions is given below.

```
Robot pose and speed in (x,z) coordinates:
x = position in x [m]
z = position in y [m]
phi = orientation [rad]
dx = speed in x [m/s]
dz = speed in z [m/s]
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
r = radius of the wheels [m]: 20.5mm 
d = distance between the wheels [m]: 52mm 
a = distance from the center of the wheels to the point of interest [m]: 50mm
```

You can use the pieces of code below to initialize the encoder sensors and to read encoder values in the main loop of your program:

To initialize encoders:
```
encoder = []
encoderNames = ['left wheel sensor', 'right wheel sensor']
for i in range(2):
    encoder.append(robot.getPositionSensor(encoderNames[i]))
    encoder[i].enable(timestep)
```

To read the encoders in the main loop:
```
    encoderValues = []
    for i in range(2):
        encoderValues.append(encoder[i].getValue())    # [rad]
```
The encoder values are incremented when the corresponding wheel moves forwards and decremented when it moves backwards.

## Conclusion
After following this lab you should know more about the implementation and limitations of odometry-based localization for mobile robots.


