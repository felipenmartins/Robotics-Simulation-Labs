"""line_following_with_HIL controller."""
# This program implements Hardware-in-the-Loop simulation of the e-puck robot.
# Ground sensor data is pre-processed and transfered to an external board 
# that must decide the next state of the robot. Communication between Webots
# and the external board is implemented via Serial port.

# Tested on Webots R2023a, on Windows 10 running Python 3.10.5 64-bit
# communicating with MicroPython v1.21.0 on generic ESP32 module with ESP32

# Author: Felipe N. Martins
# Date: 11 September 2024

from controller import Robot
import numpy as np

#-------------------------------------------------------
# Open serial port to communicate with the microcontroller

import serial
try:
    # Change the port parameter according to your system
    ser =  serial.Serial(port='COM7', baudrate=115200, timeout=5) 
except:
    print("Communication failed. Check the cable connections and serial settings 'port' and 'baudrate'.")
    raise
    
#-------------------------------------------------------
# Initialize variables

TIME_STEP = 64
MAX_SPEED = 6.28

speed = 0.4 * MAX_SPEED

# create the Robot instance for the simulation.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

# states
states = ['forward', 'turn_right', 'turn_left', 'stop']
current_state = states[3]

#-------------------------------------------------------
# Initialize devices

# proximity sensors
# See: https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?tab-language=python#understand-the-e-puck-model
ps = []
psNames = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(timestep)

# ground sensors
gs = []
gsNames = ['gs0', 'gs1', 'gs2']
for i in range(3):
    gs.append(robot.getDevice(gsNames[i]))
    gs[i].enable(timestep)

# motors    
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#-------------------------------------------------------
# Main loop:
# perform simulation steps until Webots is stopping the controller
# Implements the see-think-act cycle

while robot.step(timestep) != -1:

    # ----- See -----

    # Update sensor readings
    gsValues = []
    for i in range(3):
        gsValues.append(gs[i].getValue())

    # Process sensor data
    line_right = gsValues[0] > 600
    line_center = gsValues[1] > 600
    line_left = gsValues[2] > 600
    
    # Build the message with the ground sensor data:
    # 0 = line detected; 1 = line not detected
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
    
    # Send message to the microcontroller 
    ser.write(msg_bytes)  

    # ----- Think -----

    # Serial communication: if something is received,
    # then update the current state
    if ser.in_waiting:
        value = str(ser.readline(), 'UTF-8')[:-2]
        current_state = value

    # Update speed according to the current state
    if current_state == 'forward':
        leftSpeed = speed
        rightSpeed = speed
            
    if current_state == 'turn_right':
        leftSpeed = 0.5 * speed
        rightSpeed = 0 * speed

    if current_state == 'turn_left':
        leftSpeed = 0 * speed
        rightSpeed = 0.5 * speed
        
    if current_state == 'stop':
        leftSpeed = 0.0
        rightSpeed = 0.0
 
    # ----- Act -----

    # Update velocity commands for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
   
    # Print sensor message and current state for debugging
    print(f'Sensor message: {msg_bytes} - Current state: {current_state}')

ser.close()
