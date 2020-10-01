# Evil Twin - Attack and Defence

## Requirements
* The code run on Unix OS (Kali, Ubuntu, etc.)
* Hardware requirements:
  - 2 network interface, such that at least one of them has the ability to be in 'monitor mode'  
    Notice that it is most likely that the internal network interface in your computer doen't have the ability to be switched to 'monitor mode', so you will need at least 1 external network interface
  - Change the ```html``` folder in the path ```/var/www/html``` to the ```html``` folder from our github
  - Give full premission to 'passwords.txt' file. You can do it by typing this command in the terminal - sudo chmod +rwx passwords.txt 
    - You can check the 'index.php' and 'passwords.txt' files, after you installed apache2, by doing the following:  
      1. Start the apache server - 'sudo service apache2 start'  
      2. Go to your browser and type in the URL '127.0.0.1', you should see the 'index.php'
      3. In the text box enter the password, you can enter a random sequence of letters and numbers just for the test
      4. Go to 'passwords.txt' file and you should see the sequence that you entered
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
  - **Install iptables -** sudo apt-get install iptables
* You can clone our codes by typing this command in the terminal - git clone https://github.com/orelrahum/evil-twin    


## Attack Part

### Files
* **wifi_attack.py**
  - **Step 1: Choosing an interface to put in 'monitor mode'**    
    Here you need to choose the newtork interface that will scan the network for possible APs (Access Points) to attack, and after that will send the deauthentication packets  
    Notice that you choose the network interface that can be switched to 'monitor mode'
  - **Step 2: Scanning the network for AP to attack**  
    Here you will see all the APs that were found in the network scan, and you need to choose the AP you want to attack. If no AP was found, you can choose either to rescan the network or to quit
  - **Step 3: Verifying that at least 1 client is connected to the AP you choose**  
    In order to attack the choosen AP we need to verify that there is at least 1 client that is connected to it. If no client was found, you can choose either to rescan for clients or to quit
  - **Step 4: Disconnect the connection between the AP from the client**  
    Here we want to disconnect between the choosen AP and client. We will do that by running 'deauth.py', this file will run in the backgroung as long as the attack is appening
  - **Step 5: Put the interface back in 'managed mode'**  
    After the attack is done we need to switched back the network interface to 'managed mode'
  
* **deauth.py**  
  Here we will send the deathentication packets from to choosen AP to the choosen client and vice versa, it will cause them to disconnect from each other  
  Notice that when this file is start running, it will run in the same terminal as the 'wifi_attack.py'. A new terminal, that will run 'fake_ap.py', will be opened in order to continue the attack

* **fake_ap.py**  
  - **Step 1:  Choosing an interface that will be used for the fake AP**  
    Here you need to choose the newtork interface that will be used as the fake AP
    Notice that this network interface needs to be in 'managed mode', and that you cannot choose the same network interface as you choose at the begining (it is still sending the deauthentication packets in the background)
  - **Step 2:  Activation of the fake AP**  
    Here  we will start running the fake AP. We will create the configuration files using 'create_conf_files.py'  
    After the fake AP will start running, the attacked client will be able to connect to it. When he will connect to it and will try to access the internet, he will be able to see only the 'index.php' that in the 'html' folder. After the client will enter the password, you will be able to see it in the 'passwords.txt' file. If you want to check this password, you can try logging with it to the AP you choose at the previous part
    Notice that the IP of the fake AP will be - 10.0.0.1
  - **Step 3:  Deactivation of the fake AP**  
    After checking that the password the client entered is correct, we can turn off the fake AP. We will delete all the configuration files we created, and reset the setting to what was before the attack 

* **create_conf_files.py**
  

* **factory_setting.py**


In this part there are 2 options, either run the code or run the machine
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
