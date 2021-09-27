import pymongo # module pour utiliser MongoDB
import ssl # module pour se connecter au serveur MongoDB
import time # allows to sleep
import datetime # module pour obtenir la date
import threading as th # module pour lancer des programmes en parallèle
import data_finder # code python pour obtenir les données issu des APIs


# =============================================================================
# get_database permet de se connecter au serveur MongoDB et à la base de données
# renvoie l'objet base de données 'Stations_Velib'
def get_database():
    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority",
                                 ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Stations_Velib']


# =============================================================================
# formater_donnees permet de mettre en forme les données
# renvoie la donnée sous forme d'objet formaté
def formater_donnees(nom="",geometry={"type": "point",'coordinates':[0,0]},
            ville="",nb_place_total=0,nb_place_dispo=0,nb_velo_dispo=0,date=""):
    result = {  'nom':nom,
                'geometry':geometry,
                'ville':ville,
                'nb_place_total':nb_place_total,
                'nb_place_dispo':nb_place_dispo,
                'nb_velo_dispo':nb_velo_dispo,
                'date':date}
    return result


# =============================================================================
# maj_collection permet se connecter aux APIs des stations Vélib de Paris,
# Rennes, Lille et Lyon et de mettres leurs données dans la collection "stations_actuelles"
# renvoie void
def maj_collection(dbname):
    collection_name = dbname["stations_actuelles"]
    #Import data from Paris
    collection_paris = data_finder.get_paris()
    for station in collection_paris['stations']:
        formated = formater_donnees( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['latitude'],station['longitude']]},
                                    ville="Paris",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=datetime.datetime.now()
        )

        collection_name.insert_one(formated)
    print("données Paris importées",end=', ')

    #Import data from Rennes
    collection_rennes = data_finder.get_rennes()
    for station in collection_rennes['stations']:
        formated = formater_donnees( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['latitude'],station['longitude']]},
                                    ville="Rennes",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=datetime.datetime.now()
        )

        collection_name.insert_one(formated)
    print("données Rennes importées",end=', ')

    #Import data From Lille
    collection_lille = data_finder.get_lille()
    for station in collection_lille:
        formated = formater_donnees( station['fields']['nom'],
                                    geometry={'type': "Point", 'coordinates':station['fields']['geo'][::-1]},
                                    ville="Lille",
                                    nb_place_total=station['fields']['nbplacesdispo'] + station['fields']['nbvelosdispo'],
                                    nb_place_dispo=station['fields']['nbplacesdispo'],
                                    nb_velo_dispo=station['fields']['nbvelosdispo'],
                                    date=datetime.datetime.now()
        )

        collection_name.insert_one(formated)
    print("données Lille importées",end=', ')

    #Import data From Lyon
    collection_name = dbname["stations_actuelles"]
    collection_lyon = data_finder.get_lyon()
    for station in collection_lyon['stations']:
        formated = formater_donnees( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['latitude'],station['longitude']]},
                                    ville="Lyon",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=datetime.datetime.now()
        )

        collection_name.insert_one(formated)
    print("données Lyon importées.")
    print("Les données des stations Vélib ont été importées avec succès.")


# =============================================================================
# initialisation permet d'initialiser la base de données ainsi que les index
# renvoie void
def initialisation():
    dbname = get_database()
    maj_collection(dbname)
    dbname["stations_actuelles"].create_index([ ( "geometry" , pymongo.GEOSPHERE ) ])
    dbname["historique"].create_index( [( "geometry" ,pymongo.GEOSPHERE )] )


# =============================================================================
# historisation permet de copier les données de "stations_actuelles" dans "historique",
# de supprimer les données de "stations_actuelles" puis d'importer des nouvelles données,
# de façon automatique, avec 2 minutes de repos
# renvoie void
def historisation():

    # fonction en thread pour actualiser les données
    def thread_principal(event_stop_thread):
        loop=True
        while loop==True :
            dbname = get_database()
            # Met les données de 'stations_actuelles' dans la collection 'historique'
            dbname['stations_actuelles'].aggregate([
                {
                    '$match': {}
                }, {
                    '$out': 'historique'
                }
                ])
            print("Les données ont mis dans 'historique'")
            # Supprime les données de 'stations_actuelles'
            dbname['stations_actuelles'].delete_many({})
            # Importe des nouvelles données dans 'stations_actuelles'
            maj_collection(dbname)
            print("Actualisation et historisation des données effectuées")

            # 2 min de repos
            #check toutes les 5 secondes, si event_stop_thread est set, pour stopper la boucle
            tempo=0
            if event_stop_thread.is_set():
                loop=False
            while (loop==True and tempo<24+1):
                time.sleep(5)
                tempo+=1
                if event_stop_thread.is_set():
                    loop=False
                    print(loop)

    # fonction en thread pour stopper l'actualisation
    def run(event):
        stop_thread=input("Pour stopper l' actualisation et l' historisation des données, taper 0 : ")
        while stop_thread!='0':
            stop_thread=input()
        event_stop_thread.set()
        print("Arrêt en cours de l'automatisation")

    #programme pour lancer les threads
    event_stop_thread=th.Event()
    thread1=th.Thread(target=thread_principal,args=(event_stop_thread,))
    thread2=th.Thread(target=run,args=(event_stop_thread,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("Fin de programme d'automatisation")
