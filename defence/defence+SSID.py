from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt 
import os
import time


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
    print(G + "\n*** Step 3: Put the interface back in 'managed mode'. *** \n")
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
    empty = input ("Press Enter to continue.........")
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
        '''
        data = {}
        data['AP'] = []
        data['AP'].append({
            'name': ap_name,
            'chnnel': ap_channel,
            'mac': ap_mac
            })
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
            '''
        # client_scan_rap()
    else: 
        # If no AP was found. 
        rescan = input("No networks were found. Do you want to rescan? [Y/n] ")
        if rescan == "n":
            print("  Sorry :(  ")
            managed_mode()
            sys.exit(0)
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
############## Deauthentication ##############
##############################################

### In this function we sniff all the packets, and if we recognize that 30 packets of deauthentication has been sniffed we will alert that there is attempt to do deathentication attack in your network's area
def deathentication_check():
	print(G + "*** Step 2: Sniffing the packets and checking for deauthentication attack. *** \n")
	print(G + "In case that will be sniffed 30 deauthentication packets, you will alerted that there is attempt to do deathentication attack in your network's area. \n")
	empty = input ("Press Enter to continue.........\n")
	print(B + "Sniffing packets for 60 second intervals...")
	print(W)
	
	sniff(iface=interface, prn = packet_handler , stop_filter=stopfilter)
	# sniff(iface="wlxc83a35c2e0b7", prn = PacketHandler , stop_filter=stopfilter)
	print(W)


### sniff(..., prn = scan_netwroks, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed. 
count = 0
def packet_handler(pkt):
	global count
	global start_time
	#print(str(pkt.type) + "               " + str(pkt.subtype))
	#    print "got pkt"
	#if pkt.haslayer(Dot11FCS)
	# 0xC - stand for deauthentication paket
	if pkt.type == 0 and pkt.subtype == 0xC:
		try:
			#print(W +  "address 1  " +str(pkt.addr1))
			#print(W +  "address 2  " +str(pkt.addr2))
			#print(W +  "address 3  " +str(pkt.addr2))
			#print ("the ap_mac is :" + ap_mac)
			if ap_mac in str(pkt.addr2):
				count=count+1
				print (O + "Deauthentication packet sniffed. Packet number: " + str(count))
		except:
			#pass
			print("An exception occurred")

	if  time.time()-start_time > 60 :
		count=0		
		print(W + "All is OK for this interval time , will start new interval")
		start_time=time.time()


def stopfilter(x):
	if count==30:
		print(R + "WARNNING!! There is deathentication attack in your area. \n It is possible that your network is under deauthentication attack!")
		return True
	else:
		return False



if __name__ == "__main__":

	if os.geteuid():
		sys.exit(R + '[**] Please run as root')
    
	print("********************************************************************** \n")
	print("************ Part 3: defence from deauthentication attack ************ \n")
	print("********************************************************************** \n")
	
	### Step 1:  Choosing an interface to put in 'monitor mode'.
	monitor_mode()
	
	### Step 2: Choosing the AP that we want to attack. 
	ap_scan_rap()
	### Step 2: Sniffing the packets and checking for deauthentication attack.
	start_time = time.time()

	deathentication_check()	
	
	###Step 3: Put the interface back in 'managed mode'.
	managed_mode()
	
	
