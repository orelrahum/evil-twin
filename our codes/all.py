import os

print("hi, do you on my  evil-twin code, enjoy")
print("pls select your your linux os:")
yourdeside = input("for start ap press 1, for stop ap press 2: \n")
linuxOS = input("for kali press 1, for ubuntu press 2: \n")
interface = input("pls enter your interface name: \n")

if yourdeside == "1":
    os.system('python3 fake_ap_start.py linuxOS')

if yourdeside == "2":
    os.system('python3 fake_ap_stop.py linuxOS interface')
