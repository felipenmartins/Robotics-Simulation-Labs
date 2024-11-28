# Bonus Lab – Robot Soccer Challenge

## Objectives
The goal of this lab is to apply everything that we learned in the course to implement a robot soccer team! 

## RCJ Soccer Simulator
For this lab, we are going to use the RoboCupJunior Soccer Simulator - SoccerSim [[1]](https://doi.org/10.3389/frobt.2022.915322), illustrated in Figure 1. SoccerSim is based on Webots and programmed in Python. 

![Soccer Sim screenshot](../SoccerSim/SoccerSim_match.gif)
 
###### Figure 1. Webots running the RCJ SoccerSim with three robots on each team.

## Tasks

Clone the [RCJ Soccer Sim](https://github.com/RoboCupJuniorTC/rcj-soccer-sim) repository to get all the files necessary. 

Each team is composed by 3 differential-drive robots. Each robot has its own Python code to control the speed of its own wheels. The code has access to the position of the robot and the ball in the field, with some noise added by the simulator. 

There is an automatic referee that takes care of the implementation of all rules, such as counting time, verifying goals, positioning the robots and ball at the beginning of the match, etc. You should not change the referee code!

Instructions on how to install and run the Soccer Simulator are avaliable [in this link](https://robocup-junior.github.io/rcj-soccersim/). The same page also has detailed explanation on how to create code for your simulated robots, including examples.

To play a match, just program your robots, hit "play", and have fun watching the game! :-)

The complete set of rules for the official RoboCup Junior Soccer Simulation competition is available [here](https://github.com/robocup-junior/soccer-rules-simulation).

Have fun!!

## Reference
[1] Martins, Felipe N., Adrián Matejov, and Marek Šuppa. "Moving robotics competitions virtual: The case study of RoboCupJunior Soccer Simulation (SoccerSim)." Frontiers in Robotics and AI, 9 (2022): 915322. Available at: [https://doi.org/10.3389/frobt.2022.915322](https://doi.org/10.3389/frobt.2022.915322)

## Main Page
Back to [main page](../README.md).
