# A note on Webots Reference Frame
The Robotics Simulation Labs, including its templates and solutions, were updated to make them compatible with the new global coordinate system adopted as default by Webots R2022a (or newer). 

In Webots R2021b and older, the robot moves in the XZ plane! Figure 1 shows the orientation of the reference frames adopted in older versions of Webots (left) and the orientation of the reference used in the newer versions (right). If you are using Webots version R2021b or older, you need to adapt your code accordingly. Please, see the [Webots R2022a release notes](https://cyberbotics.com/doc/blog/Webots-2022-a-release) for more details.

![Webots Reference Frame](https://raw.githubusercontent.com/cyberbotics/webots/released/docs/blog/images/flu-enu.png) 

Figure 1. Orientation of the reference frames used in old (left) and new (right) Webots versions [(source)](https://cyberbotics.com/doc/blog/Webots-2022-a-release).

## Main Page
Back to [main page](../README.md).
