# Domoticz-Aldes
### Domoticz plugin for Aldes T One Air product

It creates based on the data from API :
- one device for connectivity
- one device for T-One Air mode
- for each room :
   - one device for the thermostat
   - one device for the temperature sensor

Plugin just needs your login / password from your Aldes account

Enjoy !

### Warning :
Aldes API is quite slow : If udpates are immediate on the server, it can take up to 5 minutes to be taken into account by the product.
Don't play too fast with commands :)

### Install the plugin:
- Go in your Domoticz directory using a command line and open the plugins directory: ```cd domoticz/plugins```
- Clone the plugin: ```git clone https://github.com/ludosaxo/Domoticz-Aldes```
- Restart Domoticz: ```sudo systemctl restart domoticz```
- Choose "Aldes T One Air Cloud" in the list of Hardware
- Enter login/password from your Aldes account to configure the plugin

### Update the plugin:
```
- cd domoticz/plugins/Domoticz-Aldes
- git pull
```


