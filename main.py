import argparse
import math
import random

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder

# Maps EEG data to a range between 0 and 255. This function uses the affine transformation.
# oldValue: EEG data from Muse
# return: int
def eeg_tranform(oldValue):
    # Formula: (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
    return (((oldValue - 0) * (255 - 0)) / (1683 - 0)) + 0

# Maps accelerometer data to a range between 0 and 179. This function uses the affine transformation.
# oldValue: accelerometer data from Muse
# return: int
def acc_tranform(oldValue):
    # Add 1 to oldValue to force the old range to be 0 - 2 in order to avoid negative cases
    oldValue++

    # Formula: (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
    return int((((oldValue - 0) * (179 - 0)) / (2 - 0)) + 0)
    
# Sends raw EEG data to /muse/eeg/raw and transformed EEG data to /muse/eeg/transformed.
# ch1, ch2, ch3, ch4: a value between 0.0 - 1682.815 uV
# return: none
# sends client a list of 4 integers
def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, num1, num2):
    # Send raw EEG data to /muse/eeg/raw
    client.send_message("/muse/eeg/raw", [int(ch1), int(ch2), int(ch3), int(ch4)])
    
    # Send transformed EEG data to /muse/eeg/transformed
    client.send_message("/muse/eeg/transformed", [eeg_tranform(ch1), eeg_tranform(ch2), eeg_tranform(ch3), eeg_tranform(ch4)])
    
# Sends raw accelerometer data to /muse/acc/raw and transformed accelerometer data to /muse/acc/transformed.
# x, y, z: a value between -1 and 1
# return: none
# sends client a list of 3 floats or integers
def acc_handler(unused_addr, args, x, y, z):
    # If values are less than -1, force values to become -1. If values are greater than 1, force values to become 1.
    if x < -1:
        x = -1
    elif x > 1
        x = 1
    
    if y < -1:
        y = -1
    elif y > 1
        y = 1
    
    if z < -1:
        z = -1
    elif z > 1
        z = 1

    # Send raw accelerometer data to /muse/acc/raw
    client.send_message("/muse/acc/raw", [x, y, z])
    
    # Send transformed accelerometer data to /muse/acc/transformed
    client.send_message("/muse/acc/transformed", [acc_tranform(x), acc_tranform(y), acc_tranform(z))
    
# Sends blink data to /muse/blink. Blink data senses whether or not user has blinked.
# blink: 1 if blinking otherwise 0
def blink_handler(unused_addr, args, blink):
    client.send_message("/muse/blink", int(blink))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        # Port number on Muse Direct to listen from
                        default=9000,
                        help="The port to listen on")
    parser.add_argument("--send",
                        type=int,
                        # Port number on Max to send data to
                        default=8000,
                        help="The port to send data")
    args = parser.parse_args()
    
    # Send data to Max
    client = udp_client.SimpleUDPClient(args.ip, args.send)
    dispatcher = dispatcher.Dispatcher()
    
    # Receive data from Muse
    # Arguments: address, handler, args (optional)
    dispatcher.map("/eeg", eeg_handler)
    dispatcher.map("/acc", acc_handler)
    dispatcher.map("/elements/blink", blink_handler)
    
    # Set up server
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()