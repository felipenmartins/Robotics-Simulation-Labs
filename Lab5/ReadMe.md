# Lab 5 - Bonus Lab – Robot Soccer Team

## Objectives
The goal of this lab is to apply everything that we learned in the course to implement a robot soccer team! If we have more than 2 groups interested, we can have a small competition. The winning team will get **10 psychological points!!!**

## RCJ Soccer Simulator
For this lab, we are going to use the RoboCup Junior Soccer Simulator (Figure 1). It is based on Webots and programmed in Python. 

![Soccer Sim screenshot](/Lab5/Soccer_Sim.jpg)
 
Figure 1. Webots running the RCJ Soccer Simulator with three robots on each team.

## Tasks

Clone the [RCJ Soccer Sim](https://github.com/felipenmartins/rcj-soccer-sim) repository to get all the files necessary. 

Each team is composed by 3 differential-drive robots. Each robot has its own Python code to control the speed of its own wheels. The code has access to the position of the robot and the ball in the field, with some noise added by the simulator. Examples of robot controllers are available in the folder [/controllers](https://github.com/felipenmartins/rcj-soccer-sim/tree/master/controllers).

More detailed explanation on how to implement code is available [here](https://github.com/felipenmartins/rcj-soccer-sim/blob/master/docs/docs/how_to.md).

There is an automatic referee that takes care of the implementation of all rules, such as counting time, verifying goals, positioning the robots and ball at the beginning of the match, etc. You should not change the referee code. 

The complete set of rules is available at:
https://github.com/RoboCupJuniorTC/soccer-rules-simulation/blob/master/rules.pdf 

**_Important_: in the RCJ Soccer Sim the reference frame is changed by the referee so that the position of the robots is actually in the XY plane (not XZ, as convention in Webots). Check the rules for details.**

Have fun!!
