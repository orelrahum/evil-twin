import os

print("hi, do you on my  evil-twin code, enjoy")
os.system('ifconfig')
interface = input("pls enter your interface name: \n")
ssid=input(" pls enter your ssid name: \n")
line="python3 fake_ap.py " + interface + " " + ssid
os.system(line)
