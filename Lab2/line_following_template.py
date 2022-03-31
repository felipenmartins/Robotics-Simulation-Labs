"""line_following_behavior controller."""
# Use this as a template to implement the line-following state-machine

from controller import Robot, DistanceSensor, Motor
import numpy as np

#-------------------------------------------------------
# Initialize variables

TIME_STEP = 64
MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

# Creat a variable to define all possible states
states = ['forward', 'turn_right', 'turn_left']
current_state = states[0]       # This is the active state

# counter: used to maintain an active state for a number of cycles
counter = 0
COUNTER_MAX = 5

#-------------------------------------------------------
# Initialize devices

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
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Update sensor readings

    gsValues = []
    for i in range(3):
        gsValues.append(gs[i].getValue())

    # Process sensor data
    # You can use the boolean variables below (TRUE or FALSE)
    line_right = gsValues[0] > 600
    line_left = gsValues[2] > 600

    # Implement the line-following state machine
 
    ######################################
    # Write your state-machine code here #
    ######################################


    # increment counter
    counter += 1
    
    print('Counter: '+ str(counter) + '. Current state: ' + current_state)

    # Set motor speeds with the values defined by the state-machine
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

    # Repeat all steps while the simulation is running.