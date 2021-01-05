import time
import sys
import ibmiotf.application
import ibmiotf.device

#Provide your IBM Watson Device Credentials
organization = "ug0cd7" # repalce it with organization ID
deviceType = "iotproject" #replace it with device type
deviceId = "1827" #repalce with device id
authMethod = "token"
authToken = "1234567890"#repalce with token

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)        
        if cmd.data['command']=='lighton':
                print("LIGHT ON")
        elif cmd.data['command'] == 'lightoff':
            print("LIGHT OFF")
                
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        T=78
        V=350
        Vol=217
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'Temperature' : T, 'Vibrations': V ,'Voltage' : Vol}}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % T, "Vibrations = %s C" % V, "Voltage = %s %%" %Vol, "to IBM Watson")

        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback
        time.sleep(30)
