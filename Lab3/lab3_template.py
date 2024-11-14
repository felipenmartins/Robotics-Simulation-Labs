"""line_following_with_localizationpy controller."""

# This program implements a state-machine based line-following behavior
# with a template for odometry-based localization for the e-puck robot.

# This code was tested on Webots R2022a, on Windows 10 running
# Python 3.9.7 64-bit

# The encoder values are incremented when the corresponding wheel moves
# forwards, and decremented when it moves backwards.
# Encoder is simulated by reading angular position of the wheels, in radians

# Author: Felipe N. Martins
# Date: 13th of April, 2020
# Update: 17 September 2021 - add comments and adjust variable names
# Update: 03 March 2022 - change the coordinate system to ENU to match the default of Webots R2022a

from controller import Robot, DistanceSensor, Motor
import numpy as np

# -------------------------------------------------------
# Initialize variables

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]
delta_t = robot.getBasicTimeStep()/1000.0    # [s]

# states
states = ['forward', 'turn_right', 'turn_left']
current_state = states[0]

# counter: used to maintain an active state for a number of cycles
counter = 0
COUNTER_MAX = 3

# Robot pose
# Adjust the initial values to match the initial robot pose in your simulation
x = -0.06    # position in x [m]
y = 0.436    # position in y [m]
phi = 0.0531  # orientation [rad]

# Robot velocity and acceleration
dx = 0.0   # speed in x [m/s]
dy = 0.0   # speed in y [m/s]
ddx = 0.0  # acceleration in x [m/s^2]
ddy = 0.0  # acceleration in y [m/s^2]

# Robot wheel speeds
wl = 0.0    # angular speed of the left wheel [rad/s]
wr = 0.0    # angular speed of the right wheel [rad/s]

# Robot linear and angular speeds
u = 0.0    # linear speed [m/s]
w = 0.0    # angular speed [rad/s]

# e-puck Physical parameters for the kinematics model (constants)
R = 0.0205    # radius of the wheels: 20.5mm [m]
D = 0.0565    # distance between the wheels: 52mm [m]
# distance from the center of the wheels to the point of interest [m]
A = 0.05

# -------------------------------------------------------
# Initialize devices

# distance sensors
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

# encoders
encoder = []
encoderNames = ['left wheel sensor', 'right wheel sensor']
for i in range(2):
    encoder.append(robot.getDevice(encoderNames[i]))
    encoder[i].enable(timestep)

oldEncoderValues = []

# motors
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#######################################################################
# Robot Localization functions - option 1
#


def get_wheels_speed(encoderValues, oldEncoderValues, delta_t):
    """Computes speed of the wheels based on encoder readings"""
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


def get_robot_speeds(wl, wr, r, d):
    """Computes robot linear and angular speeds"""
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


def get_robot_pose(u, w, x_old, y_old, phi_old, delta_t):
    """Updates robot pose based on heading and linear and angular speeds"""
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


#######################################################################
# Robot Localization functions - option 2
#
def get_robot_displacement(encoderValues, oldEncoderValues, r, d):
    """Computes linear and angular displacement of the robot"""
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


def get_robot_pose2(lin_disp, ang_disp, x_old, y_old, phi_old):
    """Updates robot pose based on heading and displacement"""
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


# -------------------------------------------------------
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

    encoderValues = []
    for i in range(2):
        encoderValues.append(encoder[i].getValue())    # [rad]

    # Update old encoder values if not done before
    if len(oldEncoderValues) < 2:
        for i in range(2):
            oldEncoderValues.append(encoder[i].getValue())

    # Process sensor data
    line_right = gsValues[0] > 600
    line_left = gsValues[2] > 600

    # Implement the line-following state machine
    if current_state == 'forward':
        # Action for the current state: update speed variables
        leftSpeed = MAX_SPEED
        rightSpeed = MAX_SPEED

        # check if it is necessary to update current_state
        if line_right and not line_left:
            current_state = 'turn_right'
            counter = 0
        elif line_left and not line_right:
            current_state = 'turn_left'
            counter = 0

    if current_state == 'turn_right':
        # Action for the current state: update speed variables
        leftSpeed = 0.8 * MAX_SPEED
        rightSpeed = 0.4 * MAX_SPEED

        # check if it is necessary to update current_state
        if counter == COUNTER_MAX:
            current_state = 'forward'

    if current_state == 'turn_left':
        # Action for the current state: update speed variables
        leftSpeed = 0.4 * MAX_SPEED
        rightSpeed = 0.8 * MAX_SPEED

        # check if it is necessary to update current_state
        if counter == COUNTER_MAX:
            current_state = 'forward'

    # increment counter
    counter += 1

    #######################################################################
    # Robot Localization - option 1
    # Using the equations for the robot kinematics based on speed

    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)

    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, R, D)

    # Compute new robot pose
    [x, y, phi] = get_robot_pose(u, w, x, y, phi, delta_t)

    #######################################################################
    # Robot Localization - option 2
    # Calculate robot displacement, intead of speed.
    # To use, uncomment the lines below and comment the previous ones.

    # Compute linear and angular displacement of the robot
    # [lin_disp, ang_disp] = get_robot_displacement(encoderValues, oldEncoderValues, R, D)

    # Compute robot new position
    # [x, y, phi] = get_robot_pose2(lin_disp, ang_disp, x, y, phi)

    #######################################################################

    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues

    # To help on debugging:
    # print('Counter: '+ str(counter), gsValues[0], gsValues[1], gsValues[2])
    # print('Counter: '+ str(counter) + '. Current state: ' + current_state)
    print(
        f'Sim time: {robot.getTime():.3f}  Pose: x={x:.2f} m, y={y:.2f} m, phi={phi:.4f} rad.')

    # Set motor speeds with the values defined by the state-machine
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

    # Repeat all steps while the simulation is running.
