import os
from scapy.all import *
from dot11_frame import Dot11Frame
import json
#import requests

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

def doData(pkt): 
    try: 
        if(pkt.haslayer(Dot11)):
            frame = Dot11Frame(pkt, iface="wlan0")

            if(frame.src == "f2:ec:8d:a5:22:dc"):
                print(frame.src, frame.dst, frame.signal_strength, frame.ssid)

                new_data = {
                    'devices': [
                        {
                            'rssi': frame.signal_strength,
                            'mac': frame.src
                        }
                    ],
                    'device_key': getserial()
                }

                data = json.dumps(new_data)
                headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

                #requests.post(url= "https://api-wifi.puhony.eu/data", data = data, headers = headers)
        
    except Exception as e:
        print(e)

def main():
    os.system("ifconfig wlan0 down")
    os.system("iwconfig wlan0 mode monitor")
    os.system("ifconfig wlan0 up")

    sniff(iface="wlan0", prn=doData)


if __name__ == '__main__':
    main()