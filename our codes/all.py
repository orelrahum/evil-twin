import os

print("hi, do you on my  evil-twin code, enjoy")
print("pls select your your linux os:")
yourdeside = input("for stop ap press 1, for start ap press 2")
linuxOS = input("for kali press 1, for ubuntu press 2")
if yourdeside == 1:
    os.system('python3 fake_ap_stop.py linuxOS')
if yourdeside == 2:
    os.system('python3 fake_ap_start.py linuxOS')
