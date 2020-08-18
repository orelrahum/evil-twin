import os
import sys

os.system('service hostapd stop')
os.system('service apache2 stop')
os.system('service dnsmasq stop')
os.system('service rpcbind stop')
os.system('killall dnsmasq')
os.system('killall hostapd')

if sys.argv[0] == 1:
    os.system('service NetworkManager start')
if sys.argv[0] == 2:
    os.system('service network-manager start')


