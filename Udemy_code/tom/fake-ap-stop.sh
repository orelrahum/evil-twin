#!/bin/sh

service hostapd stop
service apache2 stop
service dnsmasq stop
service rpcbind stop
killall dnsmasq
killall hostapd
service network-manager start
systemctl enable systemd-resolved.service
systemctl start systemd-resolved.service

