# Domoticz-Aldes
Domoticz plugin from  Aldes T One Air product

It creates based on the data fromAPI :
- one entity for connectivity
- one entity for T-One Air mode
- for each room defined :
   - one entity per thermostat
   - one entity per temperature sensor

Plugin just needs your login / password from your Aldes account

Enjoy !

Install the plugin:
- Go in your Domoticz directory using a command line and open the plugins directory: cd domoticz/plugins
- Clone the plugin: git clone https://github.com/ludosaxo/Domoticz-Aldes
- Restart Domoticz: sudo systemctl restart domoticz
- Choose "Aldes" in the list of Hardware
- Enter login/password from your Aldes account to configure the plugin

Warning :
Aldes API is quite slow : If udpates are immediate on the server, it can take up to 5 minutes to be taken into account by the product.
Don't play too fast with commands :)
