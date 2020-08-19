import os

print("hi, do you on my  evil-twin code, enjoy")
linuxOS = input("for kali press 1, for ubuntu press 2: \n")
os.system('ifconfig')
interface = input("pls enter your interface name: \n")
ssid=input(" pls enter your ssid name: \n")
line="python3 fake_ap.py " + linuxOS +" " + interface + " " + ssid
os.system(line)
