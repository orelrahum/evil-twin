import os

print("hi, do you on my  evil-twin code, enjoy")
yourdeside = input("for start ap press 1, for stop ap press 2: \n")
linuxOS = input("for kali press 1, for ubuntu press 2: \n")


if yourdeside == "1":
    interface = input("pls enter your interface name: \n")
    ssid=input(" pls enter your ssid name: \n")
    line="python3 fake_ap_start.py " + linuxOS +" " + interface + " " + ssid
    os.system(line)

if yourdeside == "2":
    line="python3 fake_ap_stop.py " + linuxOS
    os.system(line)
