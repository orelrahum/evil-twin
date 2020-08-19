#!/bin/sh

systemctl stop systemd-resolved.service
systemctl disable systemd-resolved.service

service network-manager stop
airmon-ng check kill
ifconfig wlxc83a35c2e0b7 10.0.0.1 netmask 255.255.255.0
route add default gw 10.0.0.1

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT

dnsmasq -C dnsmasq.conf
hostapd hostapd.conf -B
service apache2 start
route add default gw 10.0.0.1



