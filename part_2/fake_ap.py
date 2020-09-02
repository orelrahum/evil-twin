import os
import sys


os.system('systemctl disable systemd-resolved.service')
os.system('systemctl stop systemd-resolved')
os.system('service NetworkManager stop')


ifconfig="ifconfig "+sys.argv[1]+" 10.0.0.1 netmask 255.255.255.0"

#os.system('airmon-ng check')
# code that replace airmon-ng
os.system(' pkill -9 hostapd')
os.system(' pkill -9 dnsmasq')
os.system(' pkill -9 wpa_supplicant')
os.system(' pkill -9 avahi-daemon')
os.system(' pkill -9 dhclient')
os.system('killall dnsmasq')
os.system('killall hostapd')


os.system(ifconfig)
os.system('route add default gw 10.0.0.1')



os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
os.system('iptables --flush')
os.system('iptables --table nat --flush')
os.system('iptables --delete-chain')
os.system('iptables --table nat --delete-chain')
os.system('iptables -P FORWARD ACCEPT')

line="python3 create_files.py "+sys.argv[1] + " " + sys.argv[2]
os.system(line)

os.system('dnsmasq -C dnsmasq.conf')
os.system('service apache2 start')
os.system('route add default gw 10.0.0.1')
os.system('hostapd hostapd.conf && route add default gw 10.0.0.1')
os.system('service apache2 start')
os.system('route add default gw 10.0.0.1')

try:
    os.remove("dnsmasq.conf")
except OSError:
    pass
try:
    os.remove("hostapd.conf")
except OSError:
    pass

close=input("for close fake ap . press 1 \n")
if close=="1":
    os.system('service NetworkManager start')
    os.system('service hostapd stop')
    os.system('service apache2 stop')
    os.system('service dnsmasq stop')
    os.system('service rpcbind stop')
    os.system('killall dnsmasq')
    os.system('killall hostapd')
    os.system('systemctl enable systemd-resolved.service') 
    os.system('systemctl start systemd-resolved')   
