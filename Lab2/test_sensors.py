"""test_sensors controller."""

from controller import Robot

#-------------------------------------------------------
# Initialize variables

MAX_SPEED = 6.28

# Create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

counter = 0
leftSpeed = 0.0
rightSpeed = 0.0

#-------------------------------------------------------
# Initialize devices

# proximity sensors
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
# Main loop:

while robot.step(timestep) != -1:

    ############################################
    #                  See                     #
    ############################################
    
    # Proximity Sensors
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    # Ground Sensors
    gsValues = []
    for i in range(3):
        gsValues.append(gs[i].getValue())

    # Encoders
    encoderValues = []
    for i in range(2):
        encoderValues.append(encoder[i].getValue())    # [rad]
    # Update old encoder values if not done before
    if len(oldEncoderValues) < 2:
        for i in range(2):
            oldEncoderValues.append(encoder[i].getValue())   
    # update old encoder values for the next cycle
    oldEncoderValues = encoderValues

    ############################################
    #                 Think                    #
    ############################################

    # Here you can implement any behavior you want, using the sensor data from the See block. 
    # For example, you can implement a line-following behavior using the ground sensors, 
    # or an obstacle avoidance behavior using the proximity sensors. 
    # You can also use the encoder values to implement a go-to-goal behavior.
    # For now, we will just set the motor speeds to zero, but you can test it with any values 
    # you want to see how the robot behaves and test the encoders.
    leftSpeed = 0.0
    rightSpeed = 0.0

    ############################################
    #                  Act                     #
    ############################################

    # Set motor speeds with the values defined by the Think block.
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

    # You can print the sensor values to the console for debugging purposes.
    # For that, let's format the values to have 2 decimals and print them in 
    # a single line for better readability.     
   
    gsValuesFormatted = [f'{val:.2f}' for val in gsValues]
    psValuesFormatted = [f'{val:.2f}' for val in psValues]
    encoderValuesFormatted = [f'{val:.2f}' for val in encoderValues]

    print(f'Counter: {counter:5d}, GS values: {gsValuesFormatted}')
    # print(f'Counter: {counter:5d}, PS values: {psValuesFormatted}')
    # print(f'Counter: {counter:5d}, Encoder values: {encoderValuesFormatted}')

    # increment counter
    counter += 1   
   
    # Repeat all steps while the simulation is running.

print('The end.')