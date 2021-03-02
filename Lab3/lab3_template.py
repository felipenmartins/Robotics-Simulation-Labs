# Use this code as a template to implement the odometry-based localization.
# The line-following state-machine is already implemented.
# The parts that need to be completed by you are indicated with a message.

# The encoder values are incremented when the corresponding wheel moves 
# forwards, and decremented when it moves backwards.
# Encoder is simulated by reading angular position of the wheels, in radians 

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
delta_t = timestep/1000.0    # [s]

# states
states = ['forward', 'turn_right', 'turn_left']
current_state = states[0]

# counter: used to maintain an active state for a number of cycles
counter = 0
counter_max = 3

# Robot pose
# ********************** ADJUST VALUES OF ROBOT POSE *************************
# Adjust the initial values to match the initial robot pose in your simulation
x = -0.44    # position in x [m]
z = 0.0    # position in y [m]
phi = 0.0  # orientation [rad]
# ****************************************************************************

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

# e-puck Physical parameters for the kinematics model
r = 0.0205    # radius of the wheels: 20.5mm [m]
d = 0.0565    # distance between the wheels: 52mm [m]
a = 0.05    # distance from the center of the wheels to the point of interest [m]

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
# Robot Localization functions
#  
# Compute speed of the wheels based on encoder readings
# Encoder values indicate the angular position of the wheel in radians
def get_wheels_speed(encoderValues, oldEncoderValues, delta_t):
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************

  
# Compute robot linear and angular speeds
def get_robot_speeds(wl, wr, r, d):
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************

  
# Compute robot pose
def get_robot_pose(u, w, z_old, x_old, phi_old, delta_t):
  # ********************************************************
  # *************** WRITE YOUR CODE HERE *******************
  # ********************************************************


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

    #######################################################################
    # Robot Localization 
    # The functions called below need to be implemented by you.
    
    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)
    
    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, r, d)
    
    # Compute new robot pose
    [z, x, phi] = get_robot_pose(u, w, z, x, phi, delta_t)

    #######################################################################

    
    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues

    # increment counter
    counter += 1
 
    print('Sim time: %6.3f ' % robot.getTime(), 
    " Pose: x=%6.2f m, z=%6.2f m, phi=%6.2f rad." % (x, z, phi))    

    # Update reference velocities for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

