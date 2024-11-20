# Lab 7 – Hardware-in-the-Loop Simulation

## Objective
Real robots are controlled by embedded hardware, so it is interesting to have a way to test it. The goal of this lab is to implement a Hardware-in-the-Loop Simulation, in which an external microcontroller board receives sensor data from the simulator and sends commands to control the simulated robot. 

## Hardware-in-the-Loop (HIL)

Simulators allow lerning robotics without the need of dealing with hardware. However, simulations hide real hardware limitations of the systems embedded in real robots. To overcome such limitation and better represent real conditions, a microcontroller can be connected to the simulator to receive sensor data and implement the robot controller. After testing, the same microcontroller can be used to control a real robot with little change in code [[1]](https://link.springer.com/chapter/10.1007/978-3-031-21065-5_44). 

HIL simulation can be implemented by connecting a microcontroller via serial port to the computer running the Webots simulation. A protocol to implement the communication between the microcontroller and the simulator needs to be defined, and the code needs to be adapted accordingly. However, all functions related to the robot control remain the same.

In this lab, we are going to use MicroPython to program an ESP32-based microcontroller board to communicate with the simulator via serial port (over USB). The board will receive sensor data from the simulator, process it, run the controller algorithm, and then send commands back to the simulator to control the simulated robot (see Figure 1).

![screenshot_Webots](../Lab7/HIL_implementation.gif)

###### Figure 1. Hardware-in-the-Loop implementation: the simulation is executed by Webots, which sends sensor data to the ESP32 board. The microcontroller calculates the desired action and sends commands back to the simulator to control the robot.

## Pre-requisites
* You must have Webots R2023a (or newer) properly configured to work with Python (see [Lab 1](../Lab1/ReadMe.md)).
* You must know how to create a robot controller in Python and how to run a simulation (see [Lab 1](../Lab1/ReadMe.md)). 
* You must know how to [implement simple behaviors](https://github.com/felipenmartins/Mobile-Robot-Control/blob/main/robot_behaviors.ipynb), and a [state machine](../Lab2/ReadMe.md) to select the robot behavior. 
* You must have a microcontroller board that can be programmed in MicroPython and can be connected to the computer via USB cable. The example code presented here was tested on a ESP32-based board. 

A popular IDE to program your microcontroller in MicroPython is Thonny. The site [Random Nerd Tutorials](https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/) provides instructions for installing Thonny IDE in Windows, Mac OS X, and Linux, flashing MicroPython software to your ESP32 board using Thonny IDE, writing and uploading code to your ESP32, and troubleshooting. 

## HIL Example

We provide two ZIP files with simple example code for you to run a HIL simulation: one file contains the simulation world shown in Figure 1, and a simple robot controller capable of communicating via serial port. The other file contains MicroPython code to interface with the simulator and control the robot.

Follow the steps below to run the example:

1. Download the file [Webots_RaFLite_HiL.zip](../Lab7/Webots_RaFLite_HiL.zip) and unzip to a folder of your preference.

2. Copy the folder `Worlds` to your Webots folder. 

3. Open Webots and **stop the running simulation**.

4. In Webots, create a new controller for the robot, and copy the code from [`line_following_with_HIL.py`](../Lab7/line_following_with_HIL.py) to it. Save the controller file.

5. Open Thonny (or the IDE you are using to program the ESP32 in MicroPython), and connect it to your ESP32.

6. Create a new file and copy the code from [`control_webots.py`](../Lab7/control_webots.py) to it. 

7. Run the code on the ESP32, then **close Thonny** (or the IDE you are using), otherwise Webots will not be able to open the serial port. Keep the ESP32 connected to your computer.

8. With the MicroPython IDE closed and the ESP32 running, run the Webots simulation. 

After executing the steps above, you should see the simulation running as in Figure 2. Please, note that Figure 2 shows Thonny open while Webots is running. This is only for illustration purposes, since **Thonny must be closed for Webots to communicate with the ESP32 via serial port**.

![Robot pose in Webots](../Lab7/HIL_Webots_Thonny.gif)

###### Figure 2. Webots screen showing the robot being controlled by the microcontroller, with sensor data and current state being printed to the console. To the right, part of the MicroPython code running on the ESP32 can be seen.


This example implements a simple line-following behavior in the ESP32 board to control the simulated robot in Webots. The pre-processed sensor data is sent from Webots to the ESP32 via serial port. The ESP32 implements the line-following state transitions according to the received sensor data, and sends the new state back to Webots. The new state is used by Webots to define the speeds of the robot wheels.

_Tip:_ Change the Webots code to force the wheels speeds to be always zero. Then, while running the simulation, move the robot manually over the line to check the message and state printed in the console.

The sections below give more details on the implementation of the serial communication and the code on Webots and on the microcontroller.

### Code running on Webots

The robot controller code running on Webots has a similar structure to the ones we saw in previous labs: it starts by importing `controller` from the `Robot` class, followed by initialization of variables and robot devices, and implements the see-think-act cycle. The main difference is the use of the Python serial library (pySerial) to send and receive data to/from the microcontroller. Documentation about the pySerial library is available at [https://pyserial.readthedocs.io/en/latest/](https://pyserial.readthedocs.io/en/latest/).

To be able to communicate via serial port, we first create a serial object `ser`, as shown in the code snippet below:

```
import serial
try:
    # Change the port parameter according to your system
    ser =  serial.Serial(port='COM13', baudrate=115200, timeout=5) 
except:
    pass
```

The parameters `port` and `baudrate` above must match the ones used by your ESP32. In my case, the ESP32 board is connected to comm port `COM13` and communicates at a baud rate of 115200 bps. The communication speed can be adjusted in code, although only a few [predefined values](https://lucidar.me/en/serialib/most-used-baud-rates-table/) are allowed. But the comm port is defined by your operating system. Refer to [this documentation page](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/establish-serial-connection.html#check-port-on-windows) for instructions on how to find out the comm port your ESP32 is using.   

Naturally, both the ESP32 and Webots need to "speak the same language" to be able to exchange information. This means that the code in both of them needs to transmit messages that the other knows the meaning of. We chose to implement communication by sending and receiving a string of characters. In the case of sensor data to be sent to the ESP32, we decided to send binary values to indicate when each sensor detects the line or not. A `message` is constructed with a sequence of ones and zeros, according to the value measured by each of the line sensors. Finally, a line feed character `\n` is added at the end, the message is encoded in 'UTF-8' format, and transmitted using the `write` method. This process is illustrated below:

```
message = ''
if line_left:
    message += '1'
else:
    message += '0'
if line_center:
    message += '1'
else:
    message += '0'
if line_right:
    message += '1'
else:
    message += '0'
msg_bytes = bytes(message + '\n', 'UTF-8')
ser.write(msg_bytes)   
```

The ESP32 and Webots are running their Python scripts at different speeds, which means that both Webots and the ESP32 will send data at any moment. So, we first need to check if a new string was received before we read the message. In Webots, this test is implemented by the method `in_waiting`, that returns `True` when there are received bytes waiting in the serial buffer. In this case, we read the string and store it in the variable `value`, that will be used to update the current state of the robot. In our example code, the string transmitted by the ESP32 is the current state (but this could be different). The code snippet below shows how this is implemented:

```
if ser.in_waiting:
    value = str(ser.readline(), 'UTF-8')[:-2] 	# ignore the last character
    current_state = value
```

Note that the last character of the string is ignored. This is done because the string sent by the ESP32 always ends with the character `\n` (line feed), but we are only interested in the other characters that contain useful information. 

### Code running on the ESP32

The ESP32 has 3 UARTs (Universal Asynchronous Receiver/Transmitter) to implement serial communication. UART0 is usually used for the MicroPython REPL (Read-Eval-Print Loop), which is the console. More information about how serial communication is implemented in the ESP32 and MicroPython is available at [here](https://www.engineersgarage.com/micropython-esp8266-esp32-uart/).

To implement serial communication in MicroPython, we begin by importing `UART` from the built-in library `machine`. To make the ESP32 able to send and receive serial data from our program using the same channel used by the REPL (the USB cable), we will need to configure UART1 to use the same pins as the REPL. However, if there is any problem and the microcontroller is reset, we need to make sure that UART0 is enabled on those pins. Therefore, in our code we first make sure that `uart` is configured to UART0:

```
from machine import Pin, UART
# First, set serial to UART0 to guarantee USB communication in case of reset
uart = UART(0, 115200, tx=1, rx=3)
```

Then, the code will wait for a button to be pressed before changing the serial port to UART1. This is done to guarantee that the serial port will only be changed after user confirmation. The code can still be stopped using Thonny before the button is pressed. After the button is pressed, the serial port is changed to UART1 and Thonny will no longer be able to communicate with the ESP32 (until it is reset). The code is implemented as follows:

```
print("Click the button to start, or the STOP button to return to REPL.")
while button.value() == True:
    sleep(0.1)
# Finally, set serial to UART1 using the same pins as UART0 to communicate via USB
uart = UART(1, 115200, tx=1, rx=3)
```

Note that the baudrate needs to be the same as in the code running in Webots (in this case, 115200 bps). The parameters `tx` and `rx` indicate the ESP32 pins that will be connected to the UART.

The ESP32 needs to read the sensor message sent by Webots, and send back the new state for the robot. Before reading the message, it uses the method `any` to check if a string is available in the serial buffer. If it is, then it uses the method `read` to read the message, then convert it to a string. As explained above, the message is a sequence of ones and zeros that correspond to the line being detected (or not) by each of the line sensors. So, each of the characters of the string is used to update the corresponding variables. The code snippet below shows how this is implemented:

```
# Check if anything was received via serial to update sensor status
if uart.any():
    msg_bytes = uart.read()    # Read all received messages
    msg_str = str(msg_bytes, 'UTF-8')  # Convert to string
    # Split it in the same order used in Webots and update sensor status

    if msg_str[-4:-3] == '1':    # line_left
        line_left = True
    else:
        line_left = False
    if msg_str[-3:-2] == '1':    # line_center
        line_center = True
    else:
        line_center = False
    if msg_str[-2:-1] == '1':     # line_right
        line_right = True
    else:
        line_right = False
```

Finally, after implementing a line-following state machine, the new state needs to be transmitted to Webots. To minimize communication, a new state will only be transmitted if it is different than the previous one. This is controlled by the flag variable `state_updated`: if it is True, then the value of `current_state` is transmitted using the method `write`, as shown below:

```
    if state_updated == True:
        uart.write(current_state + ' \n')
        state_updated = False
```

## Tasks

First, put the example described above to work using your own ESP32. Please, note that the MicroPython example code considers that there are a few buttons and LEDs connected to specific pins of the ESP32: you need to adjust the code to match your hardware.

Then, modify the code to improve the line following behavior. Your robot must follow the most outer line of the field, which means it will only turn if cannot continue moving forwards. The robot should always go back to the line if, for any reason, it runs away from it. You are free to change the code as you prefer (communication messages, number of states, speeds of the motors etc.). 

## Solution
No solution is provided for this lab.

## Conclusion
After following this lab you should know how to implement hardware-in-the-loop simulation to control a simulated robot from a microcontroller connected via serial port.

## Reference
[[1] Lima, José, Felipe N. Martins, and Paulo Costa. "Teaching Practical Robotics During the COVID-19 Pandemic: A Case Study on Regular and Hardware-in-the-Loop Simulations." Iberian Robotics Conference. Cham: Springer International Publishing, 2022.](https://link.springer.com/chapter/10.1007/978-3-031-21065-5_44)

## Next Lab
Go to [BONUS](../SoccerSim/ReadMe.md) - Robot Soccer Challenge

Back to [main page](../README.md).
