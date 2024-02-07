# Domoticz-Aldes

### Plugin Domoticz pour le T.One® Air d'Aldes

Le plugin crée sur la base des données définie dans l'application :
- un device pour le status de connectivité
- un device pour le mode du T.One
- Pour chaque pièce ayant un thermostat :
   - un device pour la consigne du thermostat
   - un device pour la température actuelle

Le plugin a juste besoin de votre login / mot de passe de votre compte Aldes

Amusez-vous bien !

### Attention :
L'API d'Aldes est très lente : même si les updates sont quasi immediats sur le serveur, ils peuvent mettre jusqu'à 5 minutes à être pris en compte par le T.One en local.
Ne jouez pas trop vite avec les commandes de thermostats ou de mode :)

### Installation du plugin:
- Allez dans votre répertoire plugins de Domoticz avec la commande suivante : ```cd domoticz/plugins```
- Clonez le plugin depuis Github : ```git clone https://github.com/ludosaxo/Domoticz-Aldes```
- Redémarrez Domoticz: ```sudo systemctl restart domoticz```
- Choisissez "Aldes T One Air Cloud" dans la liste déroulante "Hardware"
- Entrez le login/mot de passe de votre compte Aldes pour configurer le plugin

### Mise à jour du plugin:
```
- cd domoticz/plugins/Domoticz-Aldes
- git pull
```

### Domoticz plugin for Aldes T.One® Air product

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


