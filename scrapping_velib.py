import requests
import json
import urllib
import urllib.error
import urllib.request
import datetime

#############################################################
##########ON COMMENCE PAR EXTRAIRE LES VILLES QUI############
###################DES CONTRATS AVEC JCDECAUX################
#############################################################

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

'''
def urls_par_contrats(villes):
    """
    Retourne les liens associés à chaque contrat
    """
    urls = []
    for ville in villes:
        urls.append("https://api.jcdecaux.com/vls/v3/stations?contract=" + str(ville) + "&apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743")
    return urls

urls = urls_par_contrats(villes_api)
'''


#############################################################
###########ON RECUPERE LES DONNEES QU'ON MET EN CSV##########
#############################################################

for ville in villes_api:
    
    url = "https://api.jcdecaux.com/vls/v3/stations?contract=" + str(ville) + "&apiKey=720018d1d90eabf26f779b2c85f07ded04e3f743" #URL qui change en fonction de la ville
    dataStation = requests.get(url)
    data = dataStation.json()
    
    # totalStands
    nbVeloDispo_total = []
    nbEmplacementDispo_total = []
    Capacite_total = []
    # mainStands
    nbVeloDispo_main = []
    nbEmplacementDispo_main = []
    Capacite_main = []
    # overflowStands 
    nbVeloDispo_overflow = []
    nbEmplacementDispo_overflow = []
    Capacite_overflow = []
    
    number = []
    nom_station = [] 
    adresse_station = []
    latitude = []
    longitude = []
    statut = []
    connecte_systeme = []
    derniere_maj = []
    
    entetes = ["nom_station","adresse_station","numero","latitude","longitude","statut"
               ,"connecte_systeme","nbVeloDispo_total","nbEmplacementDispo_total","Capacite_total"
               ,"nbVeloDispo_main","nbEmplacementDispo_main","Capacite_main",
               "nbVeloDispo_overflow","nbEmplacementDispo_overflow","Capacite_overflow","derniere_maj"]
    
        
        
    for stations in data:
        nbVeloDispo_total.append(stations['totalStands']['availabilities']['bikes'])
        nbEmplacementDispo_total.append(stations['totalStands']['availabilities']['stands'])
        Capacite_total.append(stations['totalStands']['capacity'])
            
        nbVeloDispo_main.append(stations['mainStands']['availabilities']['bikes'])
        nbEmplacementDispo_main.append(stations['mainStands']['availabilities']['stands'])
        Capacite_main.append(stations['mainStands']['capacity'])
        
        if stations['overflow'] == False:
            nbVeloDispo_overflow.append(0)
            nbEmplacementDispo_overflow.append(0)
            Capacite_overflow.append(0)
        else : 
            nbVeloDispo_overflow.append(stations['overflowStands']['availabilities']['bikes'])
            nbEmplacementDispo_overflow.append(stations['overflowStands']['availabilities']['stands'])
            Capacite_overflow.append(stations['overflowStands']['capacity'])
        
        if stations['connected'] == False:
            connecte_systeme.append('0') #0 si pas connecté
        else : 
            connecte_systeme.append('1') #1 si connecté
            
        number.append(stations['number'])
        nom_station.append(stations['name'])
        adresse_station.append(stations['address'].replace(',',' '))
        latitude.append(stations['position']['latitude'])
        longitude.append(stations['position']['longitude'])
        statut.append(stations['status'])
        derniere_maj.append(stations['lastUpdate'])

#############################################################
####################POUR ECRIRE LES CSV######################
#############################################################

"""    
    with open("velib_" + str(ville) + ".csv", "w", encoding="utf-8") as outf:
        ligneEntete = ",".join(entetes) + "\n"
        outf.write(ligneEntete)
        for i in range(len(data)):
            outf.write(nom_station[i] + "," + adresse_station[i] + "," + str(number[i]) 
            + "," + str(latitude[i]) + "," + str(longitude[i]) + "," + statut[i] + "," + connecte_systeme[i] 
            + "," + str(nbVeloDispo_total[i]) + "," + str(nbEmplacementDispo_total[i]) + ","
            + str(Capacite_total[i]) + "," + str(nbVeloDispo_main[i]) + "," + str(nbEmplacementDispo_main[i]) + ","
            + str(Capacite_main[i]) + "," + str(nbVeloDispo_overflow[i]) + "," + str(nbEmplacementDispo_overflow[i]) + ","
            + str(Capacite_overflow[i]) + "," + str(derniere_maj[i]) + "\n")
"""           
        


#############################################################
#############################################################
            

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

