# Evil Twin - Attack and Defence

<!-- ----------------------------------------------------------------------- -->
<!-- ------------------ Requirements for running the code ------------------ -->
<!-- ----------------------------------------------------------------------- -->

## Requirements ##

* The code run on Unix OS (Kali, Ubuntu, etc.)
* Hardware requirements:
  - 2 network interface, such that at least one of them has the ability to be in 'monitor mode'  
    Notice that it is most likely that the internal network interface in your computer doen't have the ability to be switched to 'monitor mode', so you will need at least 1 external network interface
   - Give full premission to ```passwords.txt``` file. You can do it by running the following command:   
  ```$ sudo chmod +rwx passwords.txt``` 
  <!-- \\Doesn't need this when using JavaScript
       - In your computer, change the ```html``` folder in the path ```/var/www/html``` to the [html](https://github.com/orelrahum/evil-twin/tree/master/html) folder from our github 
       - Give full premission to ```passwords.txt``` file. You can do it by running the following command:   
       ```$ sudo chmod +rwx passwords.txt``` 
       - You can check the ```index.php``` and ```passwords.txt``` files, after you installed apache2, by doing the following:  
         1. Start the apache server: ```$ sudo service apache2 start```  
         2. Go to your browser and type in the URL ```http://127.0.0.1``` or ```http://localhost```, you should see the ```index.php```
         3. In the text box enter the password, you can enter a random sequence of letters and numbers just for the test
         4. Go to ```passwords.txt``` file and you should see the sequence that you entered -->
* Requirements:
  - Update package manager:   
  ```$ sudo apt-get update```  
  ```$ sudo apt-get upgrade```
  <!-- \\Doesn't need apache2 when using JavaScript
      - Install apache2:   
      ```$ sudo apt install apache2``` -->
  - Install node-js:  
  ```$ sudo apt install nodejs```
  - Install npm:  
  ```$ sudo apt install npm```
  - Install express (require for js):  
  ```$ npm install express```
  - Install body-parser (require for js):  
  ```$ npm install body-parser```
  - Install node-wifi (require for js):  
  ```$ npm install node-wifi```
  - Install php:   
  ```$ sudo apt install php libapache2-mod-php```
  - Once the php is installed restart the Apache service:   
  ```$ sudo systemctl restart apache2```
  - Install python3:   
  ```$ sudo apt-get install python3.6```
  - Install pip3:   
  ```$ sudo apt install python3-pip``` 
  - Install scapy:   
  ```$ sudo pip3 install --pre scapy[complete]``` 
  - Install gnome-terminal:   
  ```$ sudo apt-get install gnome-terminal``` 
  - Install hostapd:   
  ```$ sudo apt-get install hostapd``` 
  - Install dnsmasq:   
  ```$ sudo apt-get install dnsmasq``` 
  - Install iptables:   
  ```$ sudo apt-get install iptables```
* You can clone our codes by typing this command in the terminal:   
 ```$ git clone https://github.com/orelrahum/evil-twin```    

<!-- ----------------------------------------------------------------------- -->
<!-- -------------- Attack Part (Files & How to run the code) -------------- -->
<!-- ----------------------------------------------------------------------- -->

## Attack Part

### Files
#### Part 1
* **wifi_attack.py**
  - **Step 1: Choosing an interface to put in 'monitor mode'**    
    Here you need to choose the network interface that will scan the network for possible APs (Access Points) to attack, and after that will send the de-authentication packets  
    Notice that you need to choose the network interface that can be switched to 'monitor mode'
  - **Step 2: Scanning the network for AP to attack**  
    Here you will see all the APs that were found in the network scan, and you need to choose the AP you want to attack. If no AP was found, you can choose either to rescan the network or to quit  
  - **Step 3: Verifying that at least 1 client connected to the AP you choose**  
    In order to attack the chosen AP we need to verify that there is at least 1 client connected to it. If no client found, you can choose either to rescan for clients or to quit  
  - **Step 4: Disconnect the connection between the AP from the client**  
    Here we want to disconnect between the chosen AP and client. We will do that by running [deauth.py](https://github.com/orelrahum/evil-twin/blob/master/attack/deauth.py), this file will run in the background as long as the attack is running
  - **Step 5: Put the interface back in 'managed mode'**  
    Once attack done, we need to switch back the network interface to 'managed mode'
  
* **deauth.py**  
  - Here we will send the de-authentication packets from to chosen AP to the chosen client and vice versa, it will cause them to disconnect from each other  
  Notice that when this file is start running, it will run in the same terminal as the ```wifi_attack.py```. A new terminal, that will run [fake_ap.py](https://github.com/orelrahum/evil-twin/blob/master/attack/fake_ap.py), will be opened in order to continue the attack  

#### Part 2
* **fake_ap.py**  
  - **Step 1:  Choosing an interface that will be used for the fake AP**  
    Here you need to choose the network interface that will be used as the fake AP  
    Notice that this network interface needs to be in 'managed mode', and that you cannot choose the same network interface as you choose at the beginning (it is still sending the de-authentication packets in the background)
  - **Step 2:  Activation of the fake AP**  
    Here  we will start running the fake AP. We will create the configuration files using [create_conf_files.py](https://github.com/orelrahum/evil-twin/blob/master/attack/create_conf_files.py)    
    After the fake AP will start running, the attacked client will be able to connect to it. After the client will connect to the fake AP and will try to access the internet, it will be able to see only the ```index.php``` that in the ```html``` folder. After the client will enter the password, you will be able to see it in the ```passwords.txt``` file  
    If you want to check this password, you can try logging with it to the AP you choose at the previous part
    Notice that the IP of the fake AP will be - ```10.0.0.1```
  - **Step 3:  Deactivation of the fake AP**  
    After checking that the password the client entered is correct, we can turn off the fake AP. We will delete all the configuration files we created, and reset the setting to what was before the attack  

* **create_conf_files.py**  
  - Here we create the hostapd and dnsmasq configuration files  

* **factory_setting.py**  
  - Delete all the configuration files we created, and reset the setting to what was before the attack 

### How to run the code
In this part there are 2 options to run the code, either run a full attack (Part 1 + Part 2) or just the fake AP (Part 2)

#### Option 1 - Full attack (Part 1 + Part 2)
  - Scanning the network for possible APs to attack
  - Choosing AP and client that is connected to the AP
  - Attack them. That is, disconnect them from each other
  - Run the fake AP  
  
  In this option the name of the fake AP will be as the name of the choosen AP
  
  In order to run full attack, do as following:
  1. Go to ```evil-twin/attack``` folder
  2. Run the command ```$ python3 wifi_attack.py``` as root (see picture below)
  3. Follow the instructions as in the code
  4. And most importantly, HAVE FUN :) 
  
  ![wifi_attack](https://github.com/orelrahum/evil-twin/blob/master/picture/wifi_attack.JPG?raw=true)

#### Option 2 - Fake AP (Part 2)
- Just run the fake AP  

In this option you need to choose the name of the fake AP

In order to run the fake AP, do as following:
  1. Go to ```evil-twin/attack``` folder
  2. Run the command ```$ python3 fake_ap.py  <your_fake_ap_name>``` as root (see picture below)
  3. Follow the instructions as in the code
  4. And most importantly, HAVE FUN :) 

![fake_ap](https://github.com/orelrahum/evil-twin/blob/master/picture/fake_ap.JPG?raw=true)

<!-- ----------------------------------------------------------------------- -->
<!-- -------------- Defence Part (Files & How to run the code) ------------- -->
<!-- ----------------------------------------------------------------------- -->

## Defence Part
### Files
#### Part 3
* **defence.py**
  - **Step 1: Choosing an interface to put in 'monitor mode'**  
  Here you need to choose the network interface that will scan for deauthentication packets in your area  
  Notice that you need to choose the network interface that can be switched to 'monitor mode'. You may choose the same network interface as you choose at the beginning
  - **Step 2: Sniffing the packets and checking for deauthentication attack**   
  Here we sniff the network's area for deauthentication packets. When we manage to capture 30 deauthentication packets, an alert message will appear  
  Notice that if you want to change the number of packets to capture, you can do it by changing  the number in ```if count==30``` in the function ```stopfilter(x)```
  - **Step 3: Put the interface back in 'managed mode'**   
  If any alert message has appeared or you want to stop the scanning for deauthentication packets, we need to switch back the network interface to 'managed mode'


### How to run the code
In order to run the defence, do as following:
   1. Go to ```evil-twin/defence``` folder
   2. Run the command ```$ python3 defence.py``` as root (see picture below)
   3. Follow the instructions as in the code
   4. And most importantly, HAVE FUN :) 
   
   ![defence](https://github.com/orelrahum/evil-twin/blob/master/picture/defence.JPG?raw=true)
   
<!-- ----------------------------------------------------------------------- -->
<!-- ------------- WebServer Part (Files & How to run the code) ------------ -->
<!-- ----------------------------------------------------------------------- -->

## Web Server Part
### Files
* **index2.js**  
  This file is the web server................
  - **HTML page**  
  The HTML that we present to the client is - ```generateHTML```
  - **GET method requests** 
  In general, the GET method requests a representation of the specified resource  
  In our case, when then client requesting for a website (any website) there is GET method request, the server will response with the ```generateHTML``` to any such a request  
  In the server side (attacker side) when there is GET requests, a message will appear informing that the client tried to enter a website  
  <!-- Notice that this work only on HTTP, and not on HTTPS ???????? -->
  - **POST method requests** 
  In general, the POST request method requests that a web server accepts the data enclosed in the body of the request message, most likely for storing it  
  In our case, when then client enter a password and click the ```Connect``` button there is POST method request, the server will response with the new ```generateHTML``` (now ```title``` has new value) to any such a request  
  In the server side (attacker side) when there is POST requests, a message will appear informing that the client entered a new password, the password will be saved in the file ```passwords.txt```  
  
  

### How to run the code
In this part there are 2 options to run the code, either run it and manually check the given password by the client, or run it and automatically check the given password by the client by using [node-wifi](https://www.npmjs.com/package/node-wifi)  
Notice that you can run this file separately to test that it works. If you run it without running the ```fake_ap.py```, no client will be able to access it  
If you run ```fake_ap.py```, it will automatically open a new terminal window and run the web server in it  

#### Option 1 - Manually check the password
In order to run and test the web server, do as following:
   1. Go to ```evil-twin/attack/html``` folder
   2. Run the command ```$ node index2.js``` as root
   3. Go to your browser and type in the URL ```http://127.0.0.1``` or ```http://localhost```, you should see the html page
   4. In the text box enter the password, you can enter a random sequence of letters and numbers just for the test
   5. Go to ```passwords.txt``` file and you should see the sequence you entered. You should also see a message with the password in the terminal window
   6. If you want to check the password, you can do it manually from another device
   7. And most importantly, HAVE FUN :) 

#### Option 2 - A utomatically check the password
In order automatically check the password you will need an extra network interface in 'managed mode'  
To run and test the web server, do as following:
   1. Go to ```evil-twin/attack/html``` folder
   2. Now you need to do some changes in the ```index2.js``` file: 
      - Uncomment the line ```const wifi = require('node-wifi'); ```
      - Uncomment the section ```const checkPassword = async (password) => { ... }; ```
      - Uncomment the line ```app.post('/password', async (req, res) => { ```
      - Comment the line ```app.post('/password', (req, res) => { ```
      - Uncomment the line ```const ans = await checkPassword(password); ```
      - Uncomment the line ```title = ans ? 'Great succeess :)' : 'The password is incorrect. :('; ```
      - Comment the line ```title = "Authenticating...\n If you wait more than 1min. the password is INCORRECT." ```
      - Don't forget to SAVE the file
   3. Run the command ```$ node index2.js <iface> <ssid>``` as root, such that ```<iface>``` is the extra network interface, and ```<ssid>``` is the name of the AP you want to try to connect to
   4. Go to your browser and type in the URL ```http://127.0.0.1``` or ```http://localhost```, you should see the html page
   5. In the text box enter a password, if you want the test the checking password part you may want to enter the correct password to the ```<ssid>```, and an incorrect password
   6. A related message, whether the password was correct or incorrect, will appear in the top of the presented HTML 
   7. Go to ```passwords.txt``` file and you should see the passwords you entered. You should also see a messages with the passwords in the terminal window
   8. And most importantly, HAVE FUN :) 

   
   
