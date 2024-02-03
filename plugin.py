# Aldes T.One Air plugin
#
# Author: Ludo, 2024


"""
<plugin key="Aldes TOne Air" name="Aldes T.One Air Cloud" author="Ludo" version="1.0.0" externallink="">
    <description>Aldes T.One Air plugin to get Temperatures, setpoints and Modes<br/>Please provide your email and password of your Aldes account</description>
    <params>
        <param field="Username" label="Username" width="200px" required="true" default="">
            <description>==== Enter username and password from your Aldes account ====</description>
        </param>
        <param field="Password" label="Password" width="200px" required="true" default="" password="true"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import urllib.parse
import json
import sys
import requests

# Unit number according devide type
# ID modem Aldes    : Modes
# ID from Aldes     : Setpoint
# ID from Aldes+100 : Temperatures

class AldesPlugin:
    def __init__(self):
        self.AuthSrv = "https://aldesiotsuite-aldeswebapi.azurewebsites.net/oauth2/token"
        self.ProductSrv = "https://aldesiotsuite-aldeswebapi.azurewebsites.net/aldesoc/v5/users/me/products"
        self.token = ""
        self.thermostat_id = 0
        self.modem = 0
        self.serialNumber = 0
        self.modes = {"A":"Off","B":"Confort","C":"Eco","D":"Prog A","E":"Prog B","F":"Clim","G":"Boost","H":"Prog C","I":"Prog D"}
        self.isConnected = False
        self.heartBeatCounter = 0
        return

    def onStart(self):
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
        Domoticz.Status("onStart called")
        #Get authenticating token
        self.authenticating()
        #Get all devices from API
        responseJson = self.getAPIData()
        #Create all deviced
        self.createDevices(responseJson)

    def authenticating(self):
        Domoticz.Status("Authenticating ...")
        Domoticz.Status("Username : "+str(Parameters["Username"]))
        Domoticz.Status("Password : "+str(Parameters["Password"]))
        login = str(Parameters["Username"])
        pwd = ["Password"])
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        data = {'grant_type':'password','username':str(login),'password':str(pwd)}
        response = requests.post(self.AuthSrv, headers=header, data=data)
        if (response.status_code == 200):
            responseJson = response.json()
            Domoticz.Status("Connection to Aldes API : token granted")
            self.token = responseJson['access_token']
        else:
            Domoticz.Error("Can not retrieve token from API")

    def createDevices(self, productData):
        #Creation of device Aldes HVAC with all modes
        Options = {
        "LevelActions":"|||||||||",
        "LevelNames":"Offline | Arrêt | Confort | Eco | Prog A | Prog B | Clim | Boost | Prog C | Prog D",
        "LevelOffHidden": "false",
        "SelectorStyle": "1"
        }
        deviceIdTOne = self.serialNumber
        Domoticz.Device(Name="TOne", Unit=1, Type=244, Subtype=73, Switchtype=2, DeviceID=deviceIdTOne, Used=1).Create()
        Domoticz.Device(Name="Mode TOne", Unit=20, Type=244, Subtype=62, Switchtype=18, DeviceID=deviceIdTOne, Options=Options, Used=1).Create()
        Domoticz.Status("New device created : TOne serial : " + str(self.serialNumber))
        
        #Creation of Setpoints and Temperature sensors
        unit=2
        for thermostat in productData["thermostats"]:
            Name = thermostat["Name"]
            deviceIdTemp = str(thermostat["ThermostatId"])
            deviceIdSetpoint = str(thermostat["ThermostatId"])
            Domoticz.Device(Name=Name, Unit=unit, Type=80, Subtype=5, DeviceID=deviceIdTemp, Used=1).Create()
            Domoticz.Status("New device created : Temperature of : " + str(Name))
            Options={'ValueStep':'1', 'ValueMin':'16', 'ValueMax':'31', 'ValueUnit':'°C'} 
            Domoticz.Device(Name=Name, Unit=unit+10, Type=242, Subtype=1, DeviceID=deviceIdSetpoint, Options=Options, Used=1).Create()
            Domoticz.Status("New device created : Setpoint of : " + str(Name))
            unit+=1

    def getAPIData(self):
        Domoticz.Status("Retrieving data from Cloud")
        header = {'Authorization': 'Bearer '+ str(self.token)}
        response = requests.get(self.ProductSrv, headers=header)
        if (response.status_code == 200):
            Domoticz.Status("Connection to Aldes API : success retrieving data")
            responseJson = response.json()
            #Get product connection status
            self.isConnected = responseJson[0]['isConnected']
            self.modem = responseJson[0]['modem']
            self.serialNumber = responseJson[0]['serial_number']
            Domoticz.Status("Device Status : "+str(self.isConnected))
            data = responseJson[0]['indicator']
            #Domoticz.Status("Device data : "+str(data))
            #Return product data
            return data
        else:
            Domoticz.Error("Can not retrieve data from API")
            return None

    def UpdateValues(self):
        productData = self.getAPIData()
        if self.isConnected:
            #Product is connected
            mode = productData['current_air_mode']
            Devices[1].Update(nValue=1,sValue=str(1))
            level = (ord(mode)-64)*10
            Devices[20].Update(nValue=level,sValue=str(level))
            if mode == 'B' or mode == 'C' or mode == 'D' or mode == 'E':
                minValue = int(productData['cmist'])
                maxValue = int(productData['cmast'])
            if mode == 'F' or mode == 'G' or mode == 'H' or mode == 'I':
                minValue = int(productData['fmist'])
                maxValue = int(productData['fmast'])
            Options={'ValueStep':'1', 'ValueMin':str(minValue), 'ValueMax':str(maxValue), 'ValueUnit':'°C'} 
            unit=2
            for thermostat in productData["thermostats"]:
                SetpointTemp = thermostat["TemperatureSet"]
                Devices[unit+10].Update(nValue=SetpointTemp,sValue=str(SetpointTemp),Options=Options)
                currentTemp = thermostat["CurrentTemperature"]
                Devices[unit].Update(nValue=0,sValue=str(currentTemp))
                unit+=1
        else:
            #Product is offline
            level = 0
            Devices[20].Update(nValue=level,sValue=str(level))

    def onHeartbeat(self):
        self.heartBeatCounter = self.heartBeatCounter - 1
        if (self.heartBeatCounter <= 0):
            self.heartBeatCounter = 30
            Domoticz.Debug("Update data from Cloud")
            self.UpdateValues()
            
            
    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Status("onCommand called:" +str(Unit)+" ("+str(Command)+"/"+str(Level)+")")
        if Unit < 20:
            self.setSetpoint(Unit, Level)
        if Unit == 20:
            self.setMode(Level)
        
    def setSetpoint(self, Unit, Level):
        urlUpdateThermostat = self.ProductSrv + "/" + self.modem + "/updateThermostats"
        idSetPoint = Devices[Unit].DeviceID
        name = str(Devices[Unit].Name)
        nameSetPoint = name[8:]
        json=[
            {
                "ThermostatId": int(idSetPoint),
                "Name": str(nameSetPoint),
                "TemperatureSet": int(Level),
            }
        ]
        header = {'accept':'text/json','Content-Type': 'text/json','Authorization': 'Bearer '+ str(self.token)}
        response = requests.patch(urlUpdateThermostat, headers=header, json=json)
        Domoticz.Status(response.status_code)
        if response.status_code == 200:
            Domoticz.Status("Successfully set Setpoint "+nameSetPoint+ " to : "+str(Level))
        
    def setMode(self, Level):
        urlChangeMode = self.ProductSrv + "/" + self.modem + "/commands"
        mode = chr(int(Level/10)+64)
        json = {
            "params": [
                str(mode)
            ],
            "jsonrpc": '2.0',
            "method": 'changeMode',
            "id": 1
        }
        header = {'accept':'text/json','Content-Type': 'text/json','Authorization': 'Bearer '+ str(self.token)}
        response = requests.post(urlChangeMode, headers=header, json=json)
        if response.status_code == 200:
            Domoticz.Status("Successfully set Mode to "+str(mode))

global _plugin
_plugin = AldesPlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

def onDeviceAdded():
    global _plugin
    _plugin.onDeviceAdded()
    # Generic helper functions

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
            Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
