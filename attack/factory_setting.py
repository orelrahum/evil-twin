import os
import sys
import threading
import time



 


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
	reset_setting() 
	remove_conf_files()
	fake_ap_off()

	
	
