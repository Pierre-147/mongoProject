import pymongo
import ssl
import time
import threading as th
import Donnees_station
import part1

def get_database():
        
    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority",
                                 ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Stations_Velib']


def maj_collection(dbname):
    collection_name = dbname["stations_actuelles"]
    #Import data from Paris
    collection_paris = part1.get_paris()
    for station in collection_paris['stations']:
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['longitude'],station['latitude']]},
                                    ville="Paris",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("données Paris importées",end=', ')

    #Import data from Rennes
    collection_rennes = part1.get_rennes()
    for station in collection_rennes['stations']:
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['longitude'],station['latitude']]},
                                    ville="Rennes",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("données Rennes importées",end=', ')

    #Import data From Lille
    collection_lille = part1.get_lille()
    for station in collection_lille:
        formated = Donnees_station.formatt( station['fields']['nom'],
                                    geometry={'type': "Point", 'coordinates':station['fields']['geo']},
                                    ville="Lille",
                                    nb_place_total=station['fields']['nbplacesdispo'] + station['fields']['nbvelosdispo'],
                                    nb_place_dispo=station['fields']['nbplacesdispo'],
                                    nb_velo_dispo=station['fields']['nbvelosdispo'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("données Lille importées",end=', ')

    #Import data From Lyon
    collection_name = dbname["stations_actuelles"]
    collection_lyon = part1.get_lyon()
    for station in collection_lyon['stations']:
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['longitude'],station['latitude']]},
                                    ville="Lyon",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("données Lyon importées.")
    print("Les données des stations Vélib ont été importées avec succès")


def historisation():
    def thread_principal(event):
        loop=True
        while loop :
            # Get the database
            dbname = get_database()
            
            # Move the data to collection 'historique'
            dbname['stations_actuelles'].aggregate([
                {
                    '$match': {}
                }, {
                    '$out': 'historique'
                }
                ])
            # Delete data  in 'station'
            print('Les données ont été historisées')
            dbname['stations_actuelles'].delete_many({})
            # Put new data
            maj_collection(dbname)
            print("Actualisation et historisation des données effectuées")
            
            #check toutes les 30 secondes, si l'event est set
            tempo=0
            if event.is_set():
                loop=False
            while loop and tempo<24+1:
                time.sleep(5)
                tempo+=1
                print('#',end='')
                if event.is_set():
                    loop=False
            print('')
            
    
    def run(event):
        stop_thread=input("Pour stopper l' actualisation et l' historisation des données, taper 1 : ")
        while stop_thread!='1':
            stop_thread=input()
        event.set()
        print("!! Arrêt de l'automatisation !!")
    
    event_stop_thread=th.Event()
    thread1=th.Thread(target=thread_principal,args=(event_stop_thread,))
    thread2=th.Thread(target=run,args=(event_stop_thread,))
    thread1.start()
    thread2.start()
    event_stop_thread.wait()
    print("Fin de programme d'automatisation")
    

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    maj_collection(dbname)

    