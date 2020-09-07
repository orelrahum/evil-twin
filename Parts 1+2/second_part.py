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

### Reset all the setting before we satrt. 
def reset_setting():
	os.system('service NetworkManager start')
	os.system('service hostapd stop')
	os.system('service dnsmasq stop')
	os.system('service rpcbind stop')
	os.system('killall dnsmasq')
	os.system('killall hostapd')
	os.system('systemctl enable systemd-resolved.service') 
	os.system('systemctl start systemd-resolved')  


if __name__ == "__main__":
	if os.geteuid():
        	sys.exit(R + '[**] Please run as root')
        
	print(B + "********************************************************************** \n")
	print("******** Part 2: Set up & upload fake AP. MOHAHA. WE ARE EVIL ******** \n")
	print("********************************************************************** \n")
	print(G + "*** Step 1:  Choosing an interface that will be used for the fake AP. *** \n")
	empty = input ("Press Enter to continue.........\n")
	print(W)
	os.system('ifconfig')
	interface = input(G + "Please enter the interface name you want to use: ")
	# ssid=input("Please enter the SSID name \n")
	reset_setting()
	essid = sys.argv[1]
	essid = essid + "_1"
	line="python3 fake_ap.py " + interface + " " + essid
	os.system(line)





