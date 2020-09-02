#!/bin/sh

service hostapd stop
service apache2 stop
service dnsmasq stop
service rpcbind stop
killall dnsmasq
killall hostapd
service NetworkManager start


