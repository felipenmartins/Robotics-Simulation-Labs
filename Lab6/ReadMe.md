# Lab 6 - Bonus Lab – Robot Soccer Team

## Objectives
The goal of this lab is to apply everything that we learned in the course to implement a robot soccer team! If we have more than 2 groups interested, we can have a small competition. The winning team will get **10 psychological points!!!**

## RCJ Soccer Simulator
For this lab, we are going to use the RoboCup Junior Soccer Simulator (Figure 1). It is based on Webots and programmed in Python. 

![Soccer Sim screenshot](../Lab6/Soccer_Sim.jpg)
 
Figure 1. Webots running the RCJ Soccer Simulator with three robots on each team.

## Tasks

Clone the [RCJ Soccer Sim](https://github.com/RoboCupJuniorTC/rcj-soccer-sim) repository to get all the files necessary. 

Each team is composed by 3 differential-drive robots. Each robot has its own Python code to control the speed of its own wheels. The code has access to the position of the robot and the ball in the field, with some noise added by the simulator. 

There is an automatic referee that takes care of the implementation of all rules, such as counting time, verifying goals, positioning the robots and ball at the beginning of the match, etc. You should not change the referee code!

Instructions on how to install and run the Soccer Simulator are avaliable [here](https://robocupjuniortc.github.io/rcj-soccer-sim/). The same page also has detailed explanation on how to code your robots, including examples.

To play a match, just program your robots, hit "play", and have fun watching the game! :-)

The complete set of rules for the official RoboCup Junior Soccer Simulation competition is available [here](https://github.com/RoboCupJuniorTC/soccer-rules-simulation/raw/master/rules.pdf).

**_Important_: in the RCJ Soccer Sim the reference frame is changed by the referee so that the position of the robots is actually in the XY plane (not XZ, as convention in Webots). Check the rules for details.**

Have fun!!

## Main Page
Back to [main page](../README.md).
