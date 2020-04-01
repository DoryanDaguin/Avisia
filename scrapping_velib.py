import requests
import json
import urllib
import urllib.error
import urllib.request
import datetime
import time


def ville_contrats():
    """
    Retourne la liste des contrats.
    """
    url_contrats = "https://api.jcdecaux.com/vls/v3/contracts?apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743"
    
    r = requests.get(url_contrats)
    json_data = json.loads(r.text)
        
    contrats_JCDecaux = []
        
    for element in json_data:
        contrats_JCDecaux.append(element['name'])
            
    contrats_JCDecaux.sort()
    return contrats_JCDecaux     


villes_api = ville_contrats()


def urls_par_contrats(villes):
    '''
    Retourne les liens associés à chaque contrat
    '''
    urls = []
    for ville in villes:
        urls.append("https://api.jcdecaux.com/vls/v3/stations?contract=" + str(ville) + "&apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743")
    return urls

urls = urls_par_contrats(villes_api)



########################################################################
#################ON ESSAYE DE RECUPERER LES DONNEES DE LYON#############
########################################################################

url = "https://api.jcdecaux.com/vls/v3/stations?contract=lyon&apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743"
dataStation = requests.get(url)
data = dataStation.json()

##########################QUELQUES DONNEES LYON#########################
nbVeloDispo = []
Capacite = []
nom_station = [] 
adresse_station = []
latitude = []
longitude = []
for station in data:
    nbVeloDispo.append(station['totalStands']['availabilities']['bikes'])
    Capacite.append(station["totalStands"]["capacity"])
    nom_station.append(station['name'])
    adresse_station.append(station['address'])
    latitude.append(station['position']['latitude'])
    longitude.append(station['position']['longitude'])

#print(nbVeloDispo)
#print(Capacite)
#print(nom_station)
#print(adresse_station)
#print(latitude)
#print(longitude)


########################################################################
#######################ON ITERE SUR TOUTES LES VILLES###################
########################################################################
  
with open("urls.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")  
        
        
"""    
with open("urls.txt", "r") as inf:
    for row in inf:
        url = row.strip()    
        response = requests.get(url)
        json_data = json.loads(response.text)
        nom_station = [] 
        adresse_station = []
        latitude = []
        longitude = []
        print("Analyse de la ligne " + row + "\n")
        for element in json_data:
            nom_station[element].append(element['name'])
            adresse_station[element].append(element['address'])
            latitude[element].append(element['position']['latitude'])
            longitude[element].append(element['position']['longitude'])
"""

#############################DONNEES DE VILNIUS########################         
"""
for i in range(37):
    print(nom_station[i] + ", " + adresse_station[i] + ", " + str(latitude[i]) + ", " + str(longitude[i]))
"""


########################################################################
########################################################################
            

def get_json(contract):
    url = "https://api.jcdecaux.com/vls/v3/stations?contract=" + str(contract) + "&apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743"
    response = requests.get(url)
    js = json.loads(response.text)
    now = datetime.datetime.now()
    for o in js:
        o["number"] = int(o["number"])
        o["banking"] = 1 if o["banking"] == "True" else 0
        o["bonus"] = 1 if o["bonus"] == "True" else 0
        
        o["totalStands"]["availabilities"]["bikes"] = int(o["totalStands"]["availabilities"]["bikes"])
        o["totalStands"]["availabilities"]["stands"] = int(o["totalStands"]["availabilities"]["stands"])
        o["totalStands"]["availabilities"]["mechanicalBikes"] = int(o["totalStands"]["availabilities"]["mechanicalBikes"])
        o["totalStands"]["availabilities"]["electricalBikes"] = int(o["totalStands"]["availabilities"]["electricalBikes"])
        o["totalStands"]["availabilities"]["electricalRemovableBatteryBikes"] = int(o["totalStands"]["availabilities"]["electricalRemovableBatteryBikes"])
        o["totalStands"]["availabilities"]["electricalInternalBatteryBikes"] = int(o["totalStands"]["availabilities"]["electricalInternalBatteryBikes"])
        o["totalStands"]["capacity"] = int(o["totalStands"]["capacity"])
        
        o["mainStands"]["availabilities"]["bikes"] = int(o["mainStands"]["availabilities"]["bikes"])
        o["mainStands"]["availabilities"]["stands"] = int(o["mainStands"]["availabilities"]["stands"])
        o["mainStands"]["availabilities"]["mechanicalBikes"] = int(o["mainStands"]["availabilities"]["mechanicalBikes"])
        o["mainStands"]["availabilities"]["electricalBikes"] = int(o["mainStands"]["availabilities"]["electricalBikes"])
        o["mainStands"]["availabilities"]["electricalRemovableBatteryBikes"] = int(o["mainStands"]["availabilities"]["electricalRemovableBatteryBikes"])
        o["mainStands"]["availabilities"]["electricalInternalBatteryBikes"] = int(o["mainStands"]["availabilities"]["electricalInternalBatteryBikes"])
        o["mainStands"]["capacity"] = int(o["mainStands"]["capacity"])
        
        o["collect_date"] = now
    return js

""" 
for ville in villes_api:
    print(get_json(ville))
"""

