"""trajectory_tracking_controller controller."""
# Use this code as a template to implement the trajectory tracking controller.
# The localization functions are already implemented.
# The parts that need to be completed by you are indicated with a message.

# The encoder values are incremented when the corresponding wheel moves 
# forwards, and decremented when it moves backwards.
# Encoder give values in radians.

# Update: 04 March 2022 - change the coordinate system to ENU to match the default of Webots R2022a

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
delta_t = timestep/1000.0    # [s]

# Robot pose
# ********************** ADJUST VALUES OF ROBOT POSE *************************
# Adjust the initial values to match the initial robot pose in your simulation
x = -0.06    # position in x [m]
y = 0.436    # position in y [m]
phi = 0.0531  # orientation [rad]
# ****************************************************************************

# Robot initial velocity and acceleration in (x,z) coordinates
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

# Physical parameters of the robot for the kinematics model
R = 0.0205    # radius of the wheels: 20.5mm [m]
D = 0.0565    # distance between the wheels: 52mm [m]
A = 0.05    # distance from the center of the wheels to the point of interest [m]

#-------------------------------------------------------
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

#-------------------------------------------------------
# Functions

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


def get_cartesian_speeds(u, w, phi, a):
    """Computes cartesian speeds of the robot"""
    dx = u * np.cos(phi) + a * w * np.sin(phi)
    dy = u * np.sin(phi) - a * w * np.cos(phi)
    dphi = w

    return dx, dy, dphi


def get_robot_pose(x_old, y_old, phi_old, dx, dy, dphi, delta_t):
    """Updates robot pose"""
    phi = phi_old + dphi * delta_t
    if phi >= np.pi:
        phi = phi - 2*np.pi
    elif phi < -np.pi:
        phi = phi + 2*np.pi
    
    x = x_old + dx * delta_t
    y = y_old + dy * delta_t

    return x, y, phi


def traj_tracking_controller(dxd, dyd, xd, yd, x, y, phi, a):
    """Updates references speeds for the robot to follow a trajectory"""
    # ********************************************************
    # *************** WRITE YOUR CODE HERE *******************
    # ********************************************************
    
    return u_ref, w_ref
    

def wheel_speed_commands(u_ref, w_ref, d, r):
    """Converts reference speeds to wheel speed commands"""
    # ********************************************************
    # *************** WRITE YOUR CODE HERE *******************
    # ********************************************************
    
    return leftSpeed, rightSpeed


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

    # Update old encoder values if not done before
    if len(oldEncoderValues) < 2:
        for i in range(2):
            oldEncoderValues.append(encoder[i].getValue())   

    #######################################################################
    # Robot Localization 
    x_old = x
    y_old = y
    phi_old = phi
    
    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)    
    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, R, D)
    # Compute cartesian speeds of the robot
    [dx, dy, dphi] = get_cartesian_speeds(u, w, phi, A)    
    # Compute new robot pose
    [x, y, phi] = get_robot_pose(x_old, y_old, phi_old, dx, dy, dphi, delta_t)

    #######################################################################
    # Robot Controller
    # Desired trajectory (you can use equations to define the trajectory):
    xd = 0.0
    yd = 0.0
    dxd = 0.0
    dyd = 0.0
    
    # Trajectory tracking controller
    [u_ref, w_ref] = traj_tracking_controller(dxd, dyd, xd, yd, x, y, phi, A)
    # Convert reference speeds to wheel speed commands
    [leftSpeed, rightSpeed] = wheel_speed_commands(u_ref, w_ref, D, R)

    #######################################################################
    
    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues

    # To help on debugging:
    print(f'Sim time: {robot.getTime():.3f}  Pose: x={x:.2f} m, y={y:.2f} m, phi={phi:.4f} rad. u_ref={u_ref:.3f} m/s, w_ref={w_ref:.3f} rad/s.')    

    # Update reference velocities for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
