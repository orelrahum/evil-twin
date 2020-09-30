# Evil Twin - Attack and Defencive

## Requirements
* This code run on Unix OS (Kali, Ubuntu, etc.)
* Hardware requirements:
  - 2 WiFi adapters, such that at least one of them has the ability to be in 'monitor mode'
  - Change the 'html' folder in the path "/var/www/html" to the 'html' folder from our github
  - Give full premission to 'passwords.txt' file. You can do it by typing this command in the terminal - sudo chmod +rwx passwords.txt 
* Software requirements:
  - sudo apt-get update  
  - sudo apt-get upgrade
  - **Install apache2 -** sudo apt install apache2
  - **Install php -** sudo apt install php libapache2-mod-php
  - **Once the php is installed restart the Apache service -** sudo systemctl restart apache2
  - **Install python3 -** sudo apt-get install python3.6
  - **Install pip3 -** sudo apt install python3-pip 
  - **Install scapy -** sudo pip3 install --pre scapy[complete] 
  - **Install gnome-terminal -** sudo apt-get install gnome-terminal 
  - **Install hostapd -** sudo apt-get install hostapd 
  - **Install dnsmasq -** sudo apt-get install dnsmasq 
* You can clone our codes by typing this command in the terminal - git clone https://github.com/orelrahum/evil-twin    


### how to run attack code
* if you want to run full attack (deauth and make fake ap)
  1. connect to attack folder
  2. run python3 wifi_attack.py
  3. follow after the instructions
  4. have fun
  
  ![wifi_attack](https://github.com/orelrahum/evil-twin/blob/master/picture/wifi_attack.JPG?raw=true)
  
* if you want to run fake access point code only
  1. connect to attack folder
  2.run python3 fake_ap.py + *your_fake_ap_name*
  3. follow after the instructions
  4. have fun

![fake_ap](https://github.com/orelrahum/evil-twin/blob/master/picture/fake_ap.JPG?raw=true)

### how to run defence code 
   1. connect to defence folder
   2. run python3 defence.py
   3. have fun
   ![defence](https://github.com/orelrahum/evil-twin/blob/master/picture/defence.JPG?raw=true)

