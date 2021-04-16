# Lab 4 – Trajectory Tracking Controller

## Objective
The goal of this lab is to implement a controller that enables the robot to follow a trajectory. The same controller can be used as a "go-to-position" controller. 

![screenshot_Webots](../screenshot_Webots.png)

## Webots Reference Frame
As mentioned in Lab 3, remember that in Webots the robot moves in the XZ plane! Figure 1 shows the orientation of the reference frames adopted in most cases (on the left) and in Webots (on the right). 

![Webots Reference Frame](../Lab3/Reference_frame_convention.png) 

Figure 1. Orientation of the reference frames used to develop our controller equations (left) and adopted by Webots (right).

## Tasks
Your main task is to write code to implement the functions below to add the controller to your line-following behavior from Lab 3. In the main loop of your program, those functions should be called in a sequence:

```
# Trajectory tracking controller
[u_ref, w_ref] = traj_tracking_controller(dzd, dxd, zd, xd, z, x, phi, a)

# Convert reference speeds to wheel speed commands
[leftSpeed, rightSpeed] = wheel_speed_commands(u_ref, w_ref, d, r)
```

I recommend you try to modify your line following code from Lab 3 to implement the controller as described above. Try doing it yourself, first. If your code is not working, or you need inspiration, you can use the [provided template](../Lab4/lab4_template.py). 

The tasks are listed below:

1. Write the function `traj_tracking_controller(dzd, dxd, zd, xd, z, x, phi, a)` to calculate reference values of linear and angular velocities. Those values should later be used to calculate the reference speeds of each wheel. Test your code before moving to the next step.
2. Write the function `wheel_speed_commands(u_ref, w_ref, d, r)` to calculate the reference speeds for the left and right wheels. Those are the values that need to be sent to the wheel controllers for the robot to follow the desired trajectory.
3. Test the trajectory tracking controller using the desired values below. You might need to adjust the controller gains.
```
xd = 0.0	# desired position x [m]
zd = 0.0	# desired position z [m]
dxd = 0.0	# desired speed in x [m/s]
dzd = 0.0	# desired speed in z [m/s]
```
4. Test different values of desired positions xd, zd and verify if the robot behaves as expected. If you keep the desired speeds as zero, changing the values of xd and zd should make the controller behave as a `go-to-position` controller. 


## Other details

To facilitate the comparison with the speeds calculated by Webots, print the values calculated by your functions, as shown in Figure 2. Position (x=0, z=0) is in the center of the track.

![Robot pose in Webots](../Lab4/Webots_screenshot_line_following_world.png)

Figure 2. Webots screenshot showing robot pose calculated by the simulator (left) and by the Python code (bottom).


### Think about the following questions

* Considering that you are using odometry-based localization, how does it affect the performance of the trajectory-tacking controller?
* What would you change in the code for the controller to work as a pose controller (final position + orientation)?

## Conclusion
After following this lab you should know how to implement moving controllers for mobile robots, especially to go to position and follow a trajectory.

## Challenge
Create a function to generate a trajectory: a vector `(xd, zd, dxd, dzd)` with position and speed for all points in the path. Plot the instantaneous value of position error. Adjust the controller gains to make your robot follow this trajectory with as little error as possible. 

## Solution
Try to implement the localization code yourself before checking the solution! After a successfull implementation, or if you need more inspiration than the template, an example code is available [here](../Lab4/trajectory_tracking_controller.py).

## Next Lab (optional)
Go to [Lab 5](../Lab5/ReadMe.md) - Robot Soccer Team

Back to [main page](../README.md).
