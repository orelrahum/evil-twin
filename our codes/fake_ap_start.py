import os
import sys
if sys.argv[0] == 1:
    os.system('service NetworkManager stop')
if sys.argv[0] == 2:
    os.system('service network-manager stop')

os.system('airmon-ng check kill')
os.system('ifconfig wlan0 10.0.0.1 netmask 255.255.255.0')
os.system('route add default gw 10.0.0.1')



os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
os.system('iptables --flush')
os.system('iptables --table nat --flush')
os.system('iptables --delete-chain')
os.system('iptables --table nat --delete-chain')
os.system('iptables -P FORWARD ACCEPT')


os.system('dnsmasq -C dnsmasq.conf')
os.system('hostapd hostapd.conf -B')
os.system('service apache2 start')
os.system('route add default gw 10.0.0.1')

