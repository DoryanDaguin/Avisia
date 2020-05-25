# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

#Importation
import time
import requests
import json
import threading 
import datetime

# Debut du decompte du temps
start_time = time.time()


#############################################################
#################ON AFFECTE LES VARIABLES####################
#############################################################
apiKey = "720018d1d90eabf26f779b2c85f07ded04e3f743"
url_c = 'https://api.jcdecaux.com/vls/v3/contracts?apiKey=' + apiKey

delai_recup_data_min = 3
#Il s'agit du délai entre les différentes périodes de récupération de données. 
#Ce délai est en minutes.

stop_collect_data = datetime.datetime.strptime('2020-04-08 15:55:00.0000', '%Y-%m-%d %H:%M:%S.%f')
#Il faut choisir un jour et une horaire de fin de collecte de données
#Si on ne veut pas de fin on met None



#############################################################
##########ON COMMENCE PAR EXTRAIRE LES VILLES QUI############
###############ONT DES CONTRATS AVEC JCDECAUX################
#############################################################

def ville_contrats(url):
    """
    Retourne la liste des villes qui ont un contrat avec JCDecaux
    @return     list, retourne une liste classée dans l'ordre alphabétique,
                quelque chose comme : ['ville1','ville2', ....,'ville25']
    """
        url_contrats = url
    #URL qui donne toutes les villes qui ont un contrat
    r = requests.get(url_contrats)
    json_data = json.loads(r.text)
    contrats_JCDecaux = []
        
    for element in json_data:
        contrats_JCDecaux.append(element['name'])     
    contrats_JCDecaux.sort()
    return contrats_JCDecaux     

villes = ville_contrats(url_c)

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


def collect_data_csv(villes_api):
    """
    Cette fonction permet de créer un CSV par ville présent dans l'API (25).
    Ces CSV sont composés de toutes les données temps-réel disponible sur l'API
    JCDecaux pour toutes les stations de chaque ville et quelques données 
    statiques.
    
        
    @param      villes_api        Toutes les villes de l'API JCDecaux récupéré 
                                  avec la fonction ville_contrats()
    """
    for ville in villes_api:
        
        url = "https://api.jcdecaux.com/vls/v3/stations?contract=" + str(ville) + "&apiKey=" + apiKey 
        #URL qui change en fonction de la ville
        dataStation = requests.get(url)
        data = dataStation.json()

        # DONNÉES STATIQUES
        number = []
        nom_station = [] 
        adresse_station = []
        latitude = []
        longitude = []

      
        # DONNÉES DYNAMIQUES
        statut = []
        connecte_systeme = []
        derniere_maj = []
        
        # données totalStands
        nbVeloDispo_total = [] # le nombre total de vélos présents
        nbEmplacementDispo_total = []  # le nombre d'emplacements libres
        Capacite_total = [] # la capacité totale d'accueil de vélo
        nbVelo_electrique_total = [] # le nombre total de vélos électriques présents
        nbVelo_mecanique_total = [] # le nombre total de vélos mécaniques présents
    
        # données mainStands
        nbVeloDispo_main = [] # le nombre total de vélos accrochés
        nbEmplacementDispo_main = [] # le nombre de points d'attache libres
        Capacite_main = [] # la capacité d'accueil de vélos en accroche physique
        
        # données overflowStands 
        nbVeloDispo_overflow = [] # le nombre de vélos présents en overflow
        nbEmplacementDispo_overflow = [] # le nombre d'emplacements overflow libres
        Capacite_overflow = [] #  la capacité d'accueil de vélos en overflow
        
        #On crée la première ligne pour notre futur CSV, il s'agit de toutes 
        #les variables qu'on veut récupérer
                   
            
        for stations in data:
            nbVeloDispo_total.append(stations['totalStands']['availabilities']['bikes'])
            nbEmplacementDispo_total.append(stations['totalStands']['availabilities']['stands'])
            Capacite_total.append(stations['totalStands']['capacity'])
            nbVelo_electrique_total.append(stations['totalStands']['availabilities']['electricalBikes'])
            nbVelo_mecanique_total.append(stations['totalStands']['availabilities']['mechanicalBikes'])
                
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
    
     
        with open("velib_" + str(ville) + ".csv", "a", encoding="utf-8") as outf:
            for i in range(len(data)):
                outf.write(str(number[i]) + "," + nom_station[i] + "," + adresse_station[i]
                + "," + str(latitude[i]) + "," + str(longitude[i]) + "," + statut[i] + "," + connecte_systeme[i] 
                + "," + str(Capacite_total[i]) + "," + str(nbEmplacementDispo_total[i]) + ","
                + str(nbVeloDispo_total[i]) + "," + str(nbVelo_mecanique_total[i]) + "," + str(nbVelo_electrique_total[i])
                + "," + str(Capacite_main[i]) + "," + str(nbEmplacementDispo_main[i]) + ","
                + str(nbVeloDispo_main[i]) + "," + str(Capacite_overflow[i]) + "," + str(nbEmplacementDispo_overflow[i]) + ","
                + str(nbVeloDispo_overflow[i]) + "," + str(derniere_maj[i]) + "\n")
                

#############################################################
############## ECRITURE DE L'EN-TÊTE DU CSV  ################
#############################################################

def csv_entete():
    """
    Cette fonction permet de créer les CSV.
    Elle permet d'écrire la première ligne, celle des variables.    
    """
    for ville in villes:
        entetes = ["numero","nom_station","adresse_station","latitude","longitude","statut"
                   ,"connecte_systeme","Capacite_total","nbEmplacementDispo_total","nbVeloDispo_total","nbVeloMecanique_dispo_total",
                   "nbVeloElectrique_dispo_total","Capacite_main","nbEmplacementDispo_main","nbVeloDispo_main",
                   "Capacite_overflow","nbEmplacementDispo_overflow","nbVeloDispo_overflow","derniere_maj"]
        
        with open("velib_" + str(ville) + ".csv", "w", encoding="utf-8") as outf:
            ligneEntete = ",".join(entetes) + "\n"
            outf.write(ligneEntete)



#############################################################
############ RECUPERATION DES DONNEES A LA MAIN #############
#############################################################
def collect_main():
    """
    Cette fonction permet automatiser la récupération des données.
    On les écrit dans les fichiers CSV créés.
    On a utilisé le multi-threading pour aller plus vite.
    Avec le programme classique le script prenait 3 secondes environ.
    Grâce au multi-threading il prend moins de 0,5 secondes.
    """
    thread1 = threading.Thread (target = collect_data_csv, args = (villes,))
    thread1.start()                   


############## COLLECTE DES DONNEES A LA MAIN ###############
#collect_main()



#############################################################
######### AUTOMATISER LA RECUPERATION DES DONNEES ###########
################## AVEC UN DELAI CHOISI #####################
#############################################################                

csv_entete() #On appelle la fonction qui créée les CSV et la ligne d'en-tête.
                
def collect_auto(delai_minutes, stop_collect):
    """
    Cette fonction permet automatiser la récupération des données au format CSV.
   
        
    @param      delai             Il s'agit du délai entre les différentes 
                                  périodes de récupération de données. Ce délai
                                  est en minutes.
    @param      stop_collect      On peut définir une heure ou l'on veut arrêter
                                  de récupérer les données. Il faut définir
                                  l'horaire ou mettre None si on veut tout le
                                  temps récupérer les données.
    """
    now = datetime.datetime.now()
    while stop_collect is None or now < stop_collect:
        now = datetime.datetime.now()
        thread1 = threading.Thread (target = collect_data_csv, args = (villes,))
        thread1.start()
        delai_secondes = 60*delai_minutes
        time.sleep(delai_secondes)



################ COLLECTE DES DONNEES AUTO ##################

collect_auto(delai_recup_data_min, stop_collect_data) #On appelle la fonction qui collecte les données automatiquement
          

        
# Affichage du temps d execution
print("Temps d execution : %s secondes." % round((time.time() - start_time),2))

