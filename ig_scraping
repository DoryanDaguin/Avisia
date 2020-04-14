# -*- coding: utf-8 -*-

#Importation
import time
import requests
import json
import threading 
import datetime
from tkinter import *

# Debut du decompte du temps
#start_time = time.time()


#############################################################
#################ON AFFECTE LES VARIABLES####################
#############################################################
apiKey = "720018d1d90eabf26f779b2c85f07ded04e3f743"
url_c = 'https://api.jcdecaux.com/vls/v3/contracts?apiKey=' + apiKey

delai_recup_data_min = 30
#Il s'agit du délai entre les différentes périodes de récupération de données. 
#Ce délai est en minutes.

#stop_collect_data = "15:52:00"
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

#csv_entete() #On appelle la fonction qui créée les CSV et la ligne d'en-tête.
                
def collect_auto(delai_minutes,stop_collect):
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
    now = str(datetime.datetime.now().time())
    while stop_collect is None or now < stop_collect:
        now = str(datetime.datetime.now().time())
        thread1 = threading.Thread (target = collect_data_csv, args = (villes,))
        thread1.start()
        delai_secondes = 60*delai_minutes
        time.sleep(delai_secondes)



################ COLLECTE DES DONNEES AUTO ##################

#collect_auto(delai_recup_data_min, stop_collect_data) #On appelle la fonction qui collecte les données automatiquement
          

        
# Affichage du temps d execution
#print("Temps d execution : %s secondes." % round((time.time() - start_time),2))




#############################################################
############ CREATION D'UNE INTERFACE GRAPHIQUE #############
#############################################################

#Création de la fenêtre
window = Tk()

#On personnalise notre fenêtre
window.title("Récupération des données API JCDecaux")
window.geometry("920x720")
window.minsize(920, 720)
window.maxsize(920, 720)
window.iconbitmap("logo.ico")
window.config(background="#7D0202")

#Créer la frame
frame = Frame(window, bg="#7D0202")
frame2 = Frame(window, bg="#7D0202")
frame3 = Frame(window, bg="#7D0202")
               
#Ajout d'un texte
label_title = Label(window, text="Collecte des données de l'API JCDecaux", font=("Helvedica",30), bg="#7D0202", fg="white")
label_title.pack(pady=10)

#Ajout d'un 2e texte
label_subtitle = Label(frame, text="                Cette interface a pour but de collecter les données des differentes stations des villes qui ont un contrat avec JCDecaux. \n"
                       , font=("Helvedica",12), bg="#7D0202", fg="white", justify="left")
label_subtitle.pack()

 
#Ajout d'un 3e texte
label_subtitle2 = Label(frame, text="Dans un premier temps, vous avez la possibilté de choisir le délai et de définir une heure d'arrêt de la collecte \nautomatique. Le délai est le temps que vous voulez entre les différents collectes automatiques. \n" 
                       , font=("Helvedica",12), bg="#7D0202", fg="white", justify="left")
label_subtitle2.pack()

#Ajout d'un input pour le délai
delai_question = Label(frame, text="Délai entre les collectes de données (en minutes) :", font=("Helvedica",12), bg="#7D0202", fg="white")
delai_question.pack(pady=15)
delai_entry = Entry(frame, font=("Helvedica",20), bg="#7D0202", fg="white", width=5)
delai_entry.pack()

#Ajout d'un input pour l'heure de fin de collecte

stop_question = Label(frame, text="Heure d'arrêt de collecte (hh:mm:ss) :", font=("Helvedica",12), bg="#7D0202", fg="white")
stop_question.pack(pady=10)

stop_entry = Entry(frame, font=("Helvedica",20), bg="#7D0202", fg="white", width=10)
stop_entry.pack()



def myClick() :
    mylabel = Label(frame, text="Vous avez choisi un délai de " + delai_entry.get() + " minutes et d'arrêter de collecter à " + stop_entry.get() + ".", font=("Helvedica",10), bg="#7D0202", fg="white")
    mylabel.pack()


myButton = Button(frame, text="Valider le temps de collecte et l'heure d'arrêt de collecte", font=("Helvedica",12) , bg="white", fg="#7D0202", command=myClick)
myButton.pack(pady=20)


#Ajout d'un 3e texte
label_subtitle2 = Label(frame2, text="      Ensuite, vous pouvez récupérer les données. Le premier bouton créé les CSV et la première ligne des variables. \n      Cette action ne doit être effectué que si les CSV ne sont pas créé, sinon cela écrasera les CSV existants. \n      Enfin, le deuxième bouton est celui qui permet de collecter les données automatiquements. \n      Celui-ci doit être actionné à chaque fois que l'on souhaite collecter des données. \n" 
                       , font=("Helvedica",12), bg="#7D0202", fg="white", justify="left")
label_subtitle2.pack(pady = 20)


#Ajout d'un bouton pour créer les CSV
button1 = Button(frame3, text="Cliquez pour créer les CSV et la ligne d'en-tête", font=("Helvedica",12) , bg="white", fg="#7D0202", command=csv_entete)
button1.pack(fill=X)

#Ajout d'un bouton qui récupère les données automatiquement
button = Button(frame3, text="Commencer la récupération de données", font=("Helvedica",12) , bg="white", fg="#7D0202", command=lambda: collect_auto(int(delai_entry.get()),stop_entry.get()))
button.pack(pady=20, fill=X)


#On ajoute les frames
frame.pack()
frame2.pack()
frame3.pack(side= RIGHT, padx=40)

#On affiche la fenêtre
window.mainloop()
