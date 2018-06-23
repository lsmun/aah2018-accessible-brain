import argparse
import math
import random

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder

list;

# Added 2 more arguments because Muse Direct sends 8 arguments
def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4, num1, num2):
    # bundle = osc_bundle_builder.OscBundleBuilder(
        # osc_bundle_builder.IMMEDIATELY)
    # msg = osc_message_builder.OscMessageBuilder(address="/SYNC")
    # msg.add_arg(ch1)
    # # Add 4 messages in the bundle, each with more arguments.
    # bundle.add_content(msg.build())
    # msg.add_arg(ch2)
    # bundle.add_content(msg.build())
    # msg.add_arg(ch3)
    # bundle.add_content(msg.build())
    # msg.add_arg(ch4)
    # bundle.add_content(msg.build())

    # sub_bundle = bundle.build()
    # # Now add the same bundle inside itself.
    # bundle.add_content(sub_bundle)
    # # The bundle has 5 elements in total now.

    # bundle = bundle.build()
    # # You can now send it via a client as described in other examples.
    
    print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4, num1, num2)
    
    list = [ch1, ch2, ch3, ch4]
    print(list)
    
    # Send OSC to /laura/eeg
    client.send_message("/laura/eeg", list)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        # Changed port to match Muse Direct
                        default=9000,
                        help="The port to listen on")
    parser.add_argument("--send",
                        type=int,
                        # Changed port to match Muse Direct
                        default=8000,
                        help="The port to send to")
    args = parser.parse_args()
    
    # Send shit to Max
    client = udp_client.SimpleUDPClient(args.ip, args.send)

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    # Fixed path
    dispatcher.map("/max/eeg", eeg_handler, "EEG")
    
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()