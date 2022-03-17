# Lab 1 – Webots Robot Simulator

## Objectives

The goal of this lab is to guide you to install, configure and familiarize yourself with Webots simulator. At the end of this lab you should be able to run Python code to control your simulated robot. 

## Webots
Webots is an open-source robotics simulator that can simulate several types of robots and sensors. It provides a complete development environment to model, program and simulate robots and the world they are in, including physics simulation. It is widely used in industry, education and research. Figure 1 shows a screenshot of Webots.

![Webots screenshot](../Lab1/Webots_screenshot.png)
Figure 1. Webots screenshot.

## Tasks
To complete this lab you have to follow the steps described below. 

1. From [https://cyberbotics.com/](https://cyberbotics.com/), download and install **Webots R2022a (or newer)** on your computer. There are versions available for Windows, macOS and Linux. 
#### _Note:_ Version R2022a or newer is higly recommended because of the global coordinate system adopted as default by Webots - in older versions the robot moves in the XZ plane, instead of the current standard XY plane. Webots is more than 1 GB - take into account the time to download and install it.

2. Follow all steps of [Webots Tutorial 1](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots) until and including **Hands-on #7**.

3. You need the 64-bit version of **Python 3.7, 3.8 or 3.9** to complete the robotics labs with Webots (currently, Webots R2022a does _**not**_ work with Python 3.10). You can [download Python from here.](https://www.python.org/downloads/) When you install Python, it is easier to **select the option “Add to PATH” during the installation** to include it on Windows PATH. After that, you must **reboot your system** before continuing with this tutorial.  

4. Depending on your system, the reference to Python 3 can be via the command `python` or `python3`. To test your Python installation (and to make sure that it is added to Windows PATH, in case of Windows), open the Command Prompt (cmd), PowerShell or Terminal and try both commands (`python` and `python3`). If Python is correctly installed (and included on Windows PATH), you should see something similar to:
```
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
  Type `exit()` to go back to the terminal/command prompt.

5. Configure Webots to work with Python: In the Webots menu, go to `Tools > Preferences > Python command` and set it to `python` or `python3` (whatever worked in the step above) to point Webots to your Python installation. If you haven't added Python to Windows PATH, you will need to indicate the full path in which Python is installed on your computer.

6. Install the libraries NumPy and OpenCV. Follow the instructions [from here.](https://cyberbotics.com/doc/guide/using-python#libraries)

7. Go back to Webots Tutorial 1 and continue with the session ["Create New Controller".](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?tab-language=python#create-a-new-controller) When you get to **Hands-on #8**, make sure that `Python` is selected as programming language.

7. Continue to follow the instructions of Tutorial 1 until **Hands-on #10** (remember to select Python to see the corresponding code). 

## Conclusion
After following the steps above, you should have Webots installed and configured to run Python code. You should know the fundamental concepts of Webots and how to write a simple program in Python to control a simulated robot.

In the following lab activities, we will control the virtual robot using Python.

## Next Lab
Go to [Lab 2](../Lab2/ReadMe.md) - Line-following behavior with State-Machine.

Back to [main page](../README.md).

## Known issues and solutions

1. If you are using Windows, you might see a message similar to the one below when you try to run the installation program for Webots. Don’t worry. Click on “More info” and then click the button “Run anyway” to proceed with the installation (see figure below).

  ![Windows message](../Lab1/windows_message.png)

2. Make sure you have the 64-bit version of Python (or higher) so that Webots work properly. Wrong versions of Python are known to cause issues.

3. If you already installed Python but cannot load it from the terminal/command prompt, or if Webots cannot find Python, you can add Python to Windows PATH system variable. To add Python to PATH, follow the instructions available [here](https://datatofish.com/add-python-to-windows-path/). **After you add Python to PATH you must reboot your system for the changes to take effect.** Note that you have to add only the path for the location where the executable is, without including "python.exe". A proper configuration is shown in the image below (the path in your computer might be different depending on your Python version and installation):

![windows_path_variable_python.png](windows_path_variable_python.png)

4. Depending on your hardware, when running Webots you might see a warning message like: 

```
WARNING: System below the minimal requirements.
Webots has detected that your system features an Intel GPU. A recent NVIDIA or AMD graphics
adapter is highly recommended to run Webots smoothly. 
 - Shadows have been deactivated.
 - Anti-aliasing has been deactivated.
```

This is not a problem for the simulations in the labs described here. The demo simulations that come with Webots can be quite heavy, though. If necessary, there are a couple of things that you can do to reduce the amount of computing power required by Webots:
- On the left side of the window, click on `WorldInfo`. Then, select `FPS` and reduce it to 20 (for example). This reduces the number of frames per second.
- Still in `WorldInfo`, click on `basicTimeStep` and increase it (for example, to 32).
- Go to `Tools -> Preferences -> OpenGL` and try to reduce `Ambient Occusion` and `Texture Quality`.

5. If you are using Linux, Webots might have problems accessing your project folder via symbolic links. A possible solution is to create a folder for the Webots projects on your home partition under your own user name. Another possibility is to install the APT version of Webots. Instructions on how to install the APT version can be found on [this link](https://www.cyberbotics.com/doc/guide/installation-procedure) (Thanks to Nick Buls for the tip).

