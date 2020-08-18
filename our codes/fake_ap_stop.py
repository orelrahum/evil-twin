import os

os.system('service hostapd stop')
os.system('service apache2 stop')
os.system('service dnsmasq stop')
os.system('service rpcbind stop')
os.system('killall dnsmasq')
os.system('killall hostapd')
os.system('service NetworkManager start')


