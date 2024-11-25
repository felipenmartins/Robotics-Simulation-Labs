# Robotics Simulation Labs
Here you will find a set of tutorials to practice robotics concepts with [Webots Open-Source Robot Simulator](https://cyberbotics.com/) and [Python](https://www.python.org/). 

This page is available at: [https://felipenmartins.github.io/Robotics-Simulation-Labs/](https://felipenmartins.github.io/Robotics-Simulation-Labs/)

![screenshot_Webots](screenshot_Webots.png)

## Objectives and Content
I teach an introductory-level course on Robotics for electrical engineering students, focusing on wheeled mobile robots. The simulation labs were created to replace the practical activities of this course during the Corona-related restrictions of 2020/2021. When first created, there were only 4 labs. Now, there are 7 labs to practice contents of:

 - Webots Robot Simulator and Python
 - Programming mobile robots
 - Finite-State machines
 - Obstacle avoidance
 - Kinematics of differential-drive robots
 - Odometry-based robot localization
 - Go-to-Goal behavior using PID controller
 - Non-linear trajectory tracking controller
 - Hardware-in-the-Loop (HIL) simulation 

Templates and solutions are presented for some labs, always in Python 3 (or MicroPython, for HIL).

## How to use
The simulation labs are presented as a series of tutorials, including references to the official Webots tutorials. The Labs are intended to be followed in sequence, starting from the first one.

Lab descriptions, templates and solutions are compatible with the global coordinate system now adopted as default by Webots (R2022a or newer). If you intend to use an older version of Webots, please [see this note](/coordinate_system/ReadMe.md). 

If you make use of the content in this page, please cite [[1]](https://link.springer.com/chapter/10.1007/978-3-031-21065-5_44).

## Accompanying Jupyter Notebooks
Extra explanation on how to implement Python code for some of the labs is available as [Jupyter Notebooks](https://github.com/felipenmartins/jupyter-notebooks). You can run the notebooks without the need of installing Webots to practice the corresponding concepts. The notebooks can be useful for understanding the fundamentals, especially because they allow step-by-step execution of the implemented functions. For now, the notebooks available are:
- [Odometry-based Localization](https://nbviewer.org/github/felipenmartins/Mobile-Robot-Control/blob/main/odometry-based_localization.ipynb) for the differential-drive robot
- [Implementation of simple robot behaviors](https://nbviewer.org/github/felipenmartins/Mobile-Robot-Control/blob/main/robot_behaviors.ipynb) for mobile robot control
- [Mobile Robot Control with PID](https://nbviewer.org/github/felipenmartins/Mobile-Robot-Control/blob/main/robot_control_with_PID.ipynb) to implement position control
- [Digital Image Processing](https://nbviewer.org/github/felipenmartins/Mobile-Robot-Control/blob/main/image_processing_example.ipynb): fundamentals and basic examples

## Content
The content of each lab is listed below:

- [Lab 1](/Lab1/ReadMe.md) - Installation and configuration of Webots and Python
- [Lab 2](/Lab2/ReadMe.md) - Line-following behavior with State Machine
- [Lab 3](/Lab3/ReadMe.md) - Odometry-based Localization
- [Lab 4](/Lab4/ReadMe.md) - Go-to-goal behavior with PID
- [Lab 5](/Lab5/ReadMe.md) - Combine Behaviors to Complete a Mission
- [Lab 6](/Lab6/ReadMe.md) - Trajectory Tracking Controller
- [Lab 7](/Lab7/README.md) - Hardware-in-the-Loop Simulation
- [BONUS](/SoccerSim/ReadMe.md) - Robot Soccer Challenge

## Reference
[1] Lima, José, Felipe N. Martins, and Paulo Costa. "Teaching Practical Robotics During the COVID-19 Pandemic: A Case Study on Regular and Hardware-in-the-Loop Simulations." Iberian Robotics Conference. Cham: Springer International Publishing, 2022. Available at: [https://link.springer.com/chapter/10.1007/978-3-031-21065-5_44](https://link.springer.com/chapter/10.1007/978-3-031-21065-5_44)

## License
This project is licensed under the terms of the [MIT license](/LICENSE).
