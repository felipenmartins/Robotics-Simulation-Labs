"""trajectory_tracking_controller controller."""

# This program implements a trajectpry tracking controller
# for the e-puck robot. 

# This code was tested on Webots R2020a, revision 1, on Windows 10 running
# Python 3.7.7 64-bit

# The encoder values are incremented when the corresponding wheel moves 
# forwards, and decremented when it moves backwards.
# Encoder give values in radians.

# Author: Felipe N. Martins
# Date: 14th of April, 2020

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

# counter: used to maintain an active state for a number of cycles
counter = 0
counter_max = 3

# Robot initial pose, velocity and acceleration in (x,z) coordinates
x = -0.44    # position in x [m]
z = 0.0    # position in y [m]
phi = 0.0  # orientation [rad]
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

# Physical parameters of the robot for the kinematics model
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

#-------------------------------------------------------
# Functions

# Compute speed of the wheels based on encoder readings
# Encoder values indicate the angular position of the wheel in radians
def get_wheels_speed(encoderValues, oldEncoderValues, delta_t):
    wl = (encoderValues[0] - oldEncoderValues[0])/delta_t
    wr = (encoderValues[1] - oldEncoderValues[1])/delta_t

    return wl, wr

# Compute robot linear and angular speeds
def get_robot_speeds(wl, wr, r, d):
    u = r/2.0 * (wr + wl)
    w = r/d * (wr - wl)

    return u, w

# Compute cartesian speeds of the robot
def get_cartesian_speeds(u, w, phi, a):
    dz = -u * np.cos(phi) + a * w * np.sin(phi)
    dx = u * np.sin(phi) - a * w * np.cos(phi)
    dphi = -w

    return dz, dx, dphi

# Compute robot pose
def get_robot_pose(z_old, x_old, phi_old, dz, dx, dphi, delta_t):
    phi = phi_old + dphi * delta_t
    if phi >= np.pi:
        phi = phi - 2*np.pi
    elif phi < -np.pi:
        phi = phi + 2*np.pi
    
    z = z_old + dz * delta_t
    x = x_old + dx * delta_t

    return z, x, phi

# Trajectory tracking controller
def traj_tracking_controller(dzd, dxd, zd, xd, z, x, phi, a):
    # Changing variables to use regular controller equation
    y = -x
    x = -z
    yd = -xd
    xd = -zd
    phi = -phi
    dyd = -dxd
    dxd = -dzd
    
    # Controller gains:
    kx = 2
    ky = 2

    # Controller matrix:
    C = np.matrix([[np.cos(phi), np.sin(phi)],
                   [-1/a*np.sin(phi), 1/a*np.cos(phi)]])

    # Position error:
    x_err = xd - x
    y_err = yd - y
    
    # If error is smaller than 2 cm, make it null:
    if (abs(x_err) < 0.01) and (abs(y_err) < 0.01):
        x_err = 0
        y_err = 0
        
    # Controller equation:
    [u_ref, w_ref] = C * np.matrix([[dxd + kx*x_err],[dyd + ky*y_err]])
    
    return u_ref, w_ref
    
# Convert reference speeds to wheel speed commands
def wheel_speed_commands(u_ref, w_ref, d, r):
    leftSpeed = float((2 * u_ref - d * w_ref) / (2 * r))
    rightSpeed = float((2 * u_ref + d * w_ref) / (2 * r))
    
    leftSpeed = np.sign(leftSpeed) * min(np.abs(leftSpeed), MAX_SPEED)
    rightSpeed = np.sign(rightSpeed) * min(np.abs(rightSpeed), MAX_SPEED)
    
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


    #######################################################################
    # Robot Localization 
    z_old = z
    x_old = x
    phi_old = phi
    
    # Compute speed of the wheels
    [wl, wr] = get_wheels_speed(encoderValues, oldEncoderValues, delta_t)    
    # Compute robot linear and angular speeds
    [u, w] = get_robot_speeds(wl, wr, r, d)
    # Compute cartesian speeds of the robot
    [dz, dx, dphi] = get_cartesian_speeds(u, w, phi, a)    
    # Compute new robot pose
    [z, x, phi] = get_robot_pose(z_old, x_old, phi_old, dz, dx, dphi, delta_t)

    #######################################################################
    # Robot Controller
    # Desired trajectory:
    xd = 0.0
    zd = 0.0 + 0.3*np.sin(0.005*counter)
    dxd = 0
    dzd = 0.3*0.005*np.cos(0.005*counter)
    
    # Trajectory tracking controller
    [u_ref, w_ref] = traj_tracking_controller(dzd, dxd, zd, xd, z, x, phi, a)
    # Convert reference speeds to wheel speed commands
    [leftSpeed, rightSpeed] = wheel_speed_commands(u_ref, w_ref, d, r)

    #######################################################################
    
    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues

    # increment counter
    counter += 1
    
    print('Sim time: %6.3f ' % robot.getTime(), 
    " Pose: x=%6.2f m, z=%6.2f m, phi=%6.2f rad. u_ref=%6.2f m/s, w_ref=%6.2f rad/s." % (x, z, phi, u_ref, w_ref))    

    # Update reference velocities for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)


