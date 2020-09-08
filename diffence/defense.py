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

def managed_mode():
    print(G + "\n*** Step 3: Reset the interface mode. *** \n")
    empty = input ("Press Enter in order to put " + interface + " in 'managed mode' .........\n")
    print(W)
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(B + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')

count=0
def PacketHandler(pkt):
	global count
	#print(str(pkt.type) + "               " + str(pkt.subtype))
	#    print "got pkt"
	#if pkt.haslayer(Dot11FCS)
	if pkt.type == 0 and pkt.subtype == 0xC:
		count=count+1
		print ("Deauth packet sniffed: " + str(count))


def stopfilter(x):
	if count==30:
		return True
	else:
		return False



if __name__ == "__main__":
    
   
	print(B + "********************************************************************** \n")
	print("***** Defense from deauthattack ***** \n")
	print("********************************************************************** \n")
	monitor_mode()
	print(G + "*** Step 2: now we sniffing all packets in your internet. *** \n")
	print(G + "*** if we will see deauthattack it will be alarted *** \n")
	print(W)
	sniff(iface="wlan0", prn = PacketHandler , stop_filter=stopfilter)
	print("warning you'r AP is under deauthattack!!!!!!!!!!")
