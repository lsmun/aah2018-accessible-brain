import argparse
import math
import random

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, num1, num2):
    # print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4, num1, num2)
    
    # Send OSC to /muse/eeg
    client.send_message("/muse/eeg/ch1", int(ch1))
    client.send_message("/muse/eeg/ch2", int(ch2))
    client.send_message("/muse/eeg/ch3", int(ch3))
    client.send_message("/muse/eeg/ch4", int(ch4))

def acc_handler(unused_addr, args, x, y, z):
    print("Acc ", x, y, z)
    
    # Send OSC to /muse/eeg
    #client.send_message("/muse/eeg/ch1", int(ch1))
    #client.send_message("/muse/eeg/ch2", int(ch2))
    #client.send_message("/muse/eeg/ch3", int(ch3))
    #client.send_message("/muse/eeg/ch4", int(ch4))

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
                        # Port number to send data to
                        default=8000,
                        help="The port to send data")
    args = parser.parse_args()
    
    # Send data to Max
    client = udp_client.SimpleUDPClient(args.ip, args.send)
    dispatcher = dispatcher.Dispatcher()
    
    # Set paths
    # Arguments: OSC Path, function, idk
    dispatcher.map("/eeg", eeg_handler, "EEG")
    dispatcher.map("/acc", acc_handler, "ACC")
    dispatcher.map("/elements/blink", blink_handler, "BLINK")
    
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()