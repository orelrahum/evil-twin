from scapy.all import *
import os

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
############## Deauthentication ##############
##############################################

### In this function we sniff all the packets, and if we recognize that 30 packets of deauthentication has been sniffed we will alert that there is attempt to do deathentication attack in your network's area
def deathentication_check()
	print(G + "*** Step 2: Sniffing the packets and checking for deauthentication attack. *** \n")
	print(G + "In case that will be sniffed 30 deauthentication packets, you will alerted that there is attempt to do deathentication attack in your network's area. \n")
	empty = input ("Press Enter to continue.........\n")
	print(W)
	sniff(iface=interface, prn = packet_handler , stop_filter=stopfilter)
	# sniff(iface="wlxc83a35c2e0b7", prn = PacketHandler , stop_filter=stopfilter)
	print(R + "WARNNING!! There is deathentication attack in your area. \n It is possible that your network is under deauthentication attack!")
	print(W)


### sniff(..., prn = scan_netwroks, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed. 
count = 0
def packet_handler(pkt):
	global count
	#print(str(pkt.type) + "               " + str(pkt.subtype))
	#    print "got pkt"
	#if pkt.haslayer(Dot11FCS)
	# 0xC - stand for deauthentication paket 
	if pkt.type == 0 and pkt.subtype == 0xC:
		count=count+1
		print ("Deauthentication packet sniffed. Packet number: " + str(count))


def stopfilter(x):
	if count==30:
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
	
	### Step 2: Sniffing the packets and checking for deauthentication attack.
	deathentication_check()	
	
	###Step 3: Put the interface back in 'managed mode'.
	managed_mode()
	
	
