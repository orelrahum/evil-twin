import os
import sys


line1="interface="+ sys.argv[1] + "\n"
line2="ssid=" + sys.argv[2] + "\n"
line3="channel=1\n"
line4="driver=nl80211\n"


try:
    os.remove("hostapd.conf")
except OSError:
    pass
hostapd_file=open("hostapd.conf", "a+")
hostapd_file.write(line1)
hostapd_file.write(line2)
hostapd_file.write(line3)
hostapd_file.write(line4)


line1="interface="+sys.argv[1]+"\n"
line2="dhcp-range=10.0.0.10,10.0.0.100,8h\n"
line3="dhcp-option=3,10.0.0.1\n"
line4="dhcp-option=6,10.0.0.1\n"
line5="address=/#/10.0.0.1\n"

try:
    os.remove("dnsmasq.conf")
except OSError:
    pass
dnsmasq_file=open("dnsmasq.conf", "a+")
dnsmasq_file.write(line1)
dnsmasq_file.write(line2)
dnsmasq_file.write(line3)
dnsmasq_file.write(line4)
dnsmasq_file.write(line5)
