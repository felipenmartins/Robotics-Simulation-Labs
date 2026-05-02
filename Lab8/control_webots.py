# Implements communication with Webots via Serial over USB.
# Works with the "line_following_with_HIL" controller in Webots.

# Tested with MicroPython v1.25.0 on ESP32 WROOM 32 dev kit board
# communicating with Webots R2023a, on Windows 11 running Python 3.10.5 64-bit

# To use ulab, you need to install a micropython interpreter that contains this
# module. In my tests, I used the this one:
# https://gitlab.com/rcolistete/micropython-firmwares/-/blob/master/ESP32/v1.12_with_ulab/ulab_v0.54.0_2020-07-29/Generic_flash-4MB/esp32_idf4_ulab_dp_thread_v1.12-663-gea4670d5a_2020-07-29.bin

# Author: Felipe N. Martins
# Date: 27 May 2025


###### Close Thonny after start running this code #######
# This is necessary because the serial port cannot be used by
# two different programs (Thonny and Webots) at the same time.


from machine import Pin, UART
from time import sleep
# import ulab


# Set serial to UART0 to guarantee USB communication in case of reset
# uart = UART(0, 115200, tx=1, rx=3)

led_board = Pin(2, Pin.OUT)     # Define ESP32 onboard LED
led_yellow = Pin(4, Pin.OUT)
led_blue = Pin(23, Pin.OUT)
led_green = Pin(22, Pin.OUT)
led_red = Pin(21, Pin.OUT)
button_left = Pin(34, Pin.IN, Pin.PULL_DOWN)
button_right = Pin(35, Pin.IN, Pin.PULL_DOWN)
# Button value is normally False. Returns True when clicked.

# Wait for the button click before changing the serial port to UART1.
# During the wait period, the program can be stopped using the STOP button.
print("Click the button on the ESP32 to continue. Then, close Thonny and run the Webots simulation.")
print("Or click STOP in Thonny to return to the REPL.")
while button_left() == False:
    sleep(0.25)
    led_board.value(not led_board())

# Set serial to UART1 using the same pins as UART0 to communicate via USB
uart = UART(1, 115200, tx=1, rx=3)

# Initial status of the line sensor: updated by Webots via serial
line_left = False
line_center = False
line_right = False

# Variables to implement the line-following state machine
current_state = 'forward'
counter = 0
COUNTER_MAX = 5
COUNTER_STOP = 50
state_updated = True

while True:
    
    ##################   See   ###################
    
    # Check if anything was received via serial to update sensor status
    if uart.any():
        msg_bytes = uart.read()    # Read all received messages
        msg_str = str(msg_bytes, 'UTF-8')  # Convert to string
        # Ignore old messages (Webots can send faster than the ESP32 can process)
        # Then split them in the same order used in Webots and update sensor status

        # line_left
        if msg_str[-4:-3] == '1':
            line_left = True
            led_blue.on()
        else:
            line_left = False
            led_blue.off()
        # line_center
        if msg_str[-3:-2] == '1':
            line_center = True
            led_green.on()
        else:
            line_center = False
            led_green.off()
        # line_right
        if msg_str[-2:-1] == '1':
            line_right = True
            led_red.on()
        else:
            line_right = False
            led_red.off()


    ##################   Think   ###################

    # Implement the line-following state machine transitions
    if current_state == 'forward':
        counter = 0
        if line_right and not line_left:
            current_state = 'turn_right'
            state_updated = True
        elif line_left and not line_right:
            current_state = 'turn_left'
            state_updated = True
        elif line_left and line_right and line_center: # lost the line
            current_state = 'turn_left'
            state_updated = True
        elif button_right.value() == True:
            current_state = 'stop'
            state_updated = True
            
    if current_state == 'turn_right':
        if counter >= COUNTER_MAX:
            current_state = 'forward'
            state_updated = True
        elif button_right.value() == True:
            current_state = 'stop'
            state_updated = True

    if current_state == 'turn_left':
        if counter >= COUNTER_MAX:
            current_state = 'forward'
            state_updated = True
        elif button_right.value() == True:
            current_state = 'stop'
            state_updated = True
            
    if current_state == 'stop':
        led_board.value(1)
        if counter >= COUNTER_STOP:
            current_state = 'forward'
            state_update = True
            led_board.value(0)
            
    
    ##################   Act   ###################

    # Send the new state when updated
    if state_updated == True:
        uart.write(current_state + '\n')
        state_updated = False

    counter += 1    # increment counter
    sleep(0.02)     # wait 0.02 seconds
   

