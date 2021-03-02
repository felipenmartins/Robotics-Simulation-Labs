"""line_following_behavior controller."""
# This program implements a state-machine based line-following behavior
# for the e-puck robot. 

# This code was tested on Webots R2020a, revision 1, on Windows 10 running
# Python 3.7.7 64-bit

# Author: Felipe N. Martins
# Date: 7th of April, 2020

from controller import Robot, DistanceSensor, Motor
import numpy as np

#-------------------------------------------------------
# Initialize variables

TIME_STEP = 64
MAX_SPEED = 6.28

speed = 1 * MAX_SPEED

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

# states
states = ['forward', 'turn_right', 'turn_left']
current_state = states[0]

# counter: used to maintain an active state for a number of cycles
counter = 0
counter_max = 5

#-------------------------------------------------------
# Initialize devices

# distance sensors
ps = []
psNames = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)

# ground sensors
gs = []
gsNames = ['gs0', 'gs1', 'gs2']
for i in range(3):
    gs.append(robot.getDistanceSensor(gsNames[i]))
    gs[i].enable(timestep)


# motors    
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


#-------------------------------------------------------
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Update sensor readings
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    gsValues = []
    for i in range(3):
        gsValues.append(gs[i].getValue())

    # Process sensor data
    line_right = gsValues[0] > 600
    line_left = gsValues[2] > 600

    # Implement the line-following state machine
    if current_state == 'forward':
        # Action for the current state
        leftSpeed = speed
        rightSpeed = speed
        # update current state if necessary
        if line_right and not line_left:
            current_state = 'turn_right'
            counter = 0
        elif line_left and not line_right:
            current_state = 'turn_left'
            counter = 0
            
    if current_state == 'turn_right':
        # Action for the current state
        leftSpeed = 0.8 * speed
        rightSpeed = 0.4 * speed
        # update current state if necessary
        if counter == counter_max:
            current_state = 'forward'

    if current_state == 'turn_left':
        # Action for the current state
        leftSpeed = 0.4 * speed
        rightSpeed = 0.8 * speed
        # update current state if necessary
        if counter == counter_max:
            current_state = 'forward'        

    # increment counter
    counter += 1
    
    #print('Counter: '+ str(counter), gsValues[0], gsValues[1], gsValues[2])
    print('Counter: '+ str(counter) + '. Current state: ' + current_state)

    # Update reference velocities for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

