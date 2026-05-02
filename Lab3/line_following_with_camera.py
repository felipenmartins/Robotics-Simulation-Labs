"""line_following_with_camera controller."""
# This program implements a line-following behavior
# for the e-puck robot suing images from the robot's camera as input,
# instead of ground sensors. 

# Author: Felipe N. Martins
# Date: 25 January 2026
# Last update: 2 May 2026

from controller import Robot 
import numpy as np
import cv2

#-------------------------------------------------------
# Initialize variables

TIME_STEP = 64
MAX_SPEED = 6.28

speed = 1 * MAX_SPEED

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())   # [ms]

# Actions for the line-following behavior
actions = ['forward', 'turn_right', 'turn_left']
current_action = actions[0]

#-------------------------------------------------------
# Initialize devices

# Camera    
camera = robot.getDevice('camera')
camera.enable(timestep)

# motors    
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#-------------------------------------------------------
# Functions to handle the images

def webots_image_to_bgr(camera):
    """
    Converts a Webots camera image to OpenCV BGR format.
    """
    width = camera.getWidth()
    height = camera.getHeight()

    # Get raw image data (bytes, BGRA)
    img_bytes = camera.getImage()

    # Convert bytes to numpy array
    img = np.frombuffer(img_bytes, dtype=np.uint8)

    # Reshape to (H, W, 4)
    img = img.reshape((height, width, 4))

    # Drop alpha channel -> BGR
    bgr = img[:, :, :3]

    return bgr


def detect_line_position(image):
    """
    Detect black line position on white floor.
    
    Returns:
        float or None:
            Normalized offset from image center.
            -1.0 = far left, +1.0 = far right
            None = line not detected
    """

    # Subsample the image for faster processing
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

    # Get image dimensions
    height, width, _ = image.shape

    # Define Region of Interest to process only part of the image
    roi_top = int(height * 0.70)
    roi_bottom = int(height * 0.90)
    roi_left = int(width * 0.20)
    roi_right = int(width * 0.80)

    # Using the Region of Interest (ROI)
    roi = image[roi_top:roi_bottom, roi_left:roi_right]

    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Gaussian blur (Convolution with unity mask for noise reduction)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Compute moments to get the centroid of the line on the blurred image
    # Invert pixel values (255-pixels) to get the mass of the black line
    moments = cv2.moments(255-blurred)

    if moments["m00"] == 0:
        return 0  # No line detected
    # Calculate the center of mass of the line in x
    cx = int(moments["m10"] / moments["m00"])

    # Normalize offset
    image_center = (roi_right - roi_left) / 2
    offset_pixels = cx - image_center
    normalized_offset = offset_pixels / image_center
    
    # Show images
    debug = image.copy()
    # Draw ROI rectangle
    cv2.rectangle(debug, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
    # Draw centroid
    cv2.circle(debug, (cx + roi_left, roi_top + int((roi_bottom - roi_top) / 2)), 5, (100, 0, 255), -1)
    # Draw center line
    cv2.line(debug, (int(width / 2), 0), (int(width / 2), height), (255, 0, 0), 1)
    
    # Display images for debugging
    cv2.imshow("Camera View", debug)
    cv2.waitKey(1)

    return normalized_offset


def detect_line_position_2(image):
    """
    Detect black line position on white floor from the binarized image.
    
    Returns:
        float or None:
            Normalized offset from image center.
            -1.0 = far left, +1.0 = far right
            None = line not detected
    """

    # Subsample the image for faster processing
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)

    # Get image dimensions
    height, width, _ = image.shape

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gaussian blur (Convolution with identity mask for noise reduction)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Sobel filter (x direction -> vertical edges)
    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x = np.abs(sobel_x)
    # Normalize Sobel result
    if np.max(sobel_x) > 0:
        sobel_x = (sobel_x / np.max(sobel_x) * 255).astype(np.uint8)
    else:
        return 0

    # Threshold to get binary image
    _, binary = cv2.threshold(sobel_x, 40, 255, cv2.THRESH_BINARY)

    # Define Region of Interest to process only part of the image
    roi_top = int(height * 0.70)
    roi_bottom = int(height * 0.90)
    roi_left = int(width * 0.20)
    roi_right = int(width * 0.80)

    # Using the Region of Interest (ROI)
    roi = binary[roi_top:roi_bottom, roi_left:roi_right]

    # Compute moments to get the centroid of the line
    moments = cv2.moments(roi)

    if moments["m00"] == 0:
        return 0  # No line detected
    # Calculate the center of mass of the line in x
    cx = int(moments["m10"] / moments["m00"])

    # Normalize offset
    image_center = (roi_right - roi_left) / 2
    offset_pixels = cx - image_center
    normalized_offset = offset_pixels / image_center
    
    # Show original and processed images
    debug = image.copy()
    # Draw ROI rectangle
    cv2.rectangle(debug, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
    # Draw centroid
    cv2.circle(debug, (cx + roi_left, roi_top + int((roi_bottom - roi_top) / 2)), 5, (100, 0, 255), -1)
    # Draw center line
    cv2.line(debug, (int(width / 2), 0), (int(width / 2), height), (255, 0, 0), 1)
    
    # Display images for debugging
    cv2.imshow("Camera View", debug)
    cv2.imshow("Binary", binary)
    cv2.waitKey(1)

    return normalized_offset



#-------------------------------------------------------
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

    ############################################
    #                  See                     #
    ############################################
    
    # Get image and convert it to BGR format
    image = webots_image_to_bgr(camera)
    # Define offset based on line position in the image
    line_offset = detect_line_position(image)

    ############################################
    #                 Think                    #
    ############################################

    # To print action taken by the robot:
    if np.abs(line_offset) < 0.1:
        current_action = 'forward'
    elif line_offset < 0:
        current_action = 'turn_left'
    else:
        current_action = 'turn_right' 
        
    # Proportional controller to steer the robot:
    leftSpeed = min((1 + line_offset) * speed, speed)
    rightSpeed = min((1 - line_offset) * speed, speed)

    ############################################
    #                  Act                     #
    ############################################
   
    # Print information
    print(f'Line offset: {line_offset:.3f} - Current action: {current_action}')

    # Update reference velocities for the motors
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)
