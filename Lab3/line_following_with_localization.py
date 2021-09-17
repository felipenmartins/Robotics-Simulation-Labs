"""line_following_with_localizationpy controller."""

# This program implements a state-machine based line-following behavior
# with odometry-based localization for the e-puck robot. 

# This code was tested on Webots R2020a, revision 1, on Windows 10 running
# Python 3.7.7 64-bit

# The encoder values are incremented when the corresponding wheel moves 
# forwards, and decremented when it moves backwards.
# Encoder is simulated by reading angular position of the wheels, in radians 

# Author: Felipe N. Martins
# Date: 13th of April, 2020

from controller import Robot, DistanceSensor, Motor
import numpy as np

#-------------------------------------------------------
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
x = -0.44    # position in x [m]
z = 0.0    # position in y [m]
phi = 0.0  # orientation [rad]

# Robot velocity and acceleration
dx = 0.0   # speed in x [m/s]
dz = 0.0   # speed in z [m/s]
ddx = 0.0  # acceleration in x [m/s^2]
ddz = 0.0  # acceleration in z [m/s^2]

# Robot wheel speeds
wl = 0.0    # angular speed of the left wheel [rad/s]
wr = 0.0    # angular speed of the right wheel [rad/s]

# Robot linear and angular speeds
u = 0.0    # linear speed [m/s]
w = 0.0    # angular speed [rad/s]

# e-puck Physical parameters for the kinematics model (constants)
R = 0.0205    # radius of the wheels: 20.5mm [m]
D = 0.0565    # distance between the wheels: 52mm [m]
A = 0.05    # distance from the center of the wheels to the point of interest [m]

# Encoder values in the previous cycle
oldEncoderValues = [0.0, 0.0]

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

# encoders
encoder = []
encoderNames = ['left wheel sensor', 'right wheel sensor']
for i in range(2):
    encoder.append(robot.getPositionSensor(encoderNames[i]))
    encoder[i].enable(timestep)
 
# motors    
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#######################################################################
# Robot Localization functions - option 1
#  

def get_wheels_speed(encoderValues, oldEncoderValues, delta_t):
    """Computes speed of the wheels based on encoder readings"""
    #Encoder values indicate the angular position of the wheel in radians
    wl = (encoderValues[0] - oldEncoderValues[0])/delta_t
    wr = (encoderValues[1] - oldEncoderValues[1])/delta_t

    return wl, wr


def get_robot_speeds(wl, wr, r, d):
    """Computes robot linear and angular speeds"""
    u = r/2.0 * (wr + wl)
    w = r/d * (wr - wl)

    return u, w


def get_robot_pose(u, w, z_old, x_old, phi_old, delta_t):
    """Updates robot pose based on heading and linear and angular speeds"""
    delta_phi = -w * delta_t
    phi = phi_old + delta_phi
    phi_avg = (phi_old + phi)/2   
    if phi >= np.pi:
        phi = phi - 2*np.pi
    elif phi < -np.pi:
        phi = phi + 2*np.pi
    
    delta_z = -u * np.cos(phi_avg) * delta_t
    delta_x = u * np.sin(phi_avg) * delta_t
    z = z_old + delta_z
    x = x_old + delta_x

    return z, x, phi


#######################################################################
# Robot Localization functions - option 2
#  
def get_robot_displacement(encoderValues, oldEncoderValues, r):
    """Computes linear and angular displacement of the robot"""
    dl = (encoderValues[0] - oldEncoderValues[0])*r
    dr = (encoderValues[1] - oldEncoderValues[1])*r
    
    lin_disp = (dr + dl)/2.0    # Linear displacement of the robot
    ang_disp = -(dr - dl)/D      # Angular displacement of the robot

    return lin_disp, ang_disp


def get_robot_pose2(lin_disp, ang_disp, z_old, x_old, phi_old):
    """Updates robot pose based on heading and displacement"""
    phi = phi_old + ang_disp
    phi_avg = (phi_old + phi)/2.0   
    if phi >= np.pi:
        phi = phi - 2*np.pi
    elif phi < -np.pi:
        phi = phi + 2*np.pi
    
    delta_z = -lin_disp * np.cos(phi_avg)
    delta_x = lin_disp * np.sin(phi_avg)
    z = z_old + delta_z
    x = x_old + delta_x

    return z, x, phi


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

    encoderValues = []
    for i in range(2):
        encoderValues.append(encoder[i].getValue())    # [rad]

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
    [z, x, phi] = get_robot_pose(u, w, z, x, phi, delta_t)

    #######################################################################
    # Robot Localization - option 2
    # Calculate robot displacement, intead of speed. 
    # To use, uncomment the lines below and comment the previous ones.

    # Compute linear and angular displacement of the robot 
    #[lin_disp, ang_disp] = get_robot_displacement(encoderValues, oldEncoderValues, r)

    # Compute robot new position
    #[z, x, phi] = get_robot_pose2(lin_disp, ang_disp, z, x, phi)

    #######################################################################
    
    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues
    

    # To help on debugging:        
    #print('Counter: '+ str(counter), gsValues[0], gsValues[1], gsValues[2])
    #print('Counter: '+ str(counter) + '. Current state: ' + current_state)
    print(f'Sim time: {robot.getTime():.3f}  Pose: x={x:.2f} m, z={z:.2f} m, phi={phi:.4f} rad.')    


    # Set motor speeds with the values defined by the state-machine
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

    # Repeat all steps while the simulation is running.

