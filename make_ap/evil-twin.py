import os

# Console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan


os.system('ifconfig')
interface = input("Please enter the interface name you want \n")
ssid=input("Please enter the SSID name \n")
line="python3 fake_ap.py " + interface + " " + ssid
os.system(line)
