Install Kali on VirtualBox:
1. Install VirtualBox and Extension Pack https://www.virtualbox.org/wiki/Downloads
- Windows hosts
- VM VirtualBox Extension Pack
2. Download Kali VirtualBox OVA Template https://www.offensive-security.com/kali-linux-vmware-virtualbox-image-download/
3. Install Kali VirtualBox OVA Template
4. Run the Kali and login kali/kali
5. Run in terminal:
sudo passwd root
enter kali than new password for root
root/root
6. Logout and login as root/root

Enable .htaccess for captive portal redirects:
1. Open /etc/apache2/sites-enabled/000-default.conf and replace to:
<VirtualHost *:80>
	#ServerName www.example.com
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html
	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn...
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	# Enable .htaccess for /var/www/html directory and its subdirectories
	 <Directory "/var/www/html">
	 Allowoverride all
	 </Directory>
</VirtualHost>
2. Run in terminal:
a2enmod rewrite

Install AP:
1. Copy html folder to var/www/ with replace
2. Open /etc/sudoers and add line:
%www-data ALL=(ALL:ALL) NOPASSWD: /sbin/iptables, /usr/sbin/arp
3. run in terminal:
apt update
apt-get install hostapd dnsmasq
4. done

Start the AP by shell script:
1. Go to var/www/html folder and open terminal by right click
2. Run in terminal:
sudo chown www-data:www-data ./*
sudo bash ap.sh wlan0 eth0 Tomiiiii
4. AP is started you done ;)

* With iwconfig command you can get names of devices on the network wlan0, eth0....
** Install wireshark for snipping post and get from http https://www.wireshark.org/download.html
