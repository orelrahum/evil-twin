# Evil-twin
## attack and defencive
 
* our code work on Unix OS,
* please make sure you have 2 wifi adapter
* before you start please make sure you make all install:
  1. git clone https://github.com/orelrahum/evil-twin    //get from github our project
  2. sudo apt-get update  
  3. sudo apt-get upgrade
  4. sudo apt install apache2 **install apache2**
  5. change exicting folder html to our html folder in the project
  6. sudo apt install python3-pip //install pip3
  7. sudo apt-get install gnome-terminal //install gnome-terminal
  8. sudo pip3 install --pre scapy[complete] install scapy
  9. sudo apt-get install hostapd //install hostapd
  10.sudo apt-get install dnsmasq //install dnsmasq

### how to run attack code
* if you want to run full attack (deauth and make fake ap)
  1. connect to attack folder
  2. run python3 wifi_attack.py
  3. follow after the instructions
  4. have fun
  
* if you want to run fake access point code only
  1. connect to attack folder
  2.run python3 fake_ap.py + *your_fake_ap_name*
  3. follow after the instructions
  4. have fun

### how too run attack code 
  1. connect to defence folder
  2. run python3 defence.py
  3. have fun


