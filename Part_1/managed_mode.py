import sys
import os

interface = sys.argv[1]
os.system('ifconfig ' + interface + ' down')
os.system('iwconfig ' + interface + ' mode managed')
os.system('ifconfig ' + interface + ' up')

print("The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
os.system('iwconfig')

