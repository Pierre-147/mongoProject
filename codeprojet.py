import pymongo
import ssl
import time
import Donnees_station
import part1

def get_database():
    
    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Stations_Velib']


def maj_collection(dbname):
    #Import data from Paris

    collection_name = dbname["stations_actuelles"]
    collection_paris = part1.get_paris()
    for station in collection_paris['stations']:
       
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['longitude'],station['latitude']]},
                                    ville="Paris",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.gmtime())
        )

        collection_name.insert_one(formated)
    print("données Paris importées",end=', ')


    #Import data from Rennes

    collection_name = dbname["stations_actuelles"]
    
    collection_rennes = part1.get_rennes()
    for station in collection_rennes['stations']:

        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "Point", 'coordinates':[station['longitude'],station['latitude']]},
                                    ville="Rennes",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.gmtime())
        )

        collection_name.insert_one(formated)
    print("données Rennes importées",end=', ')



    #Import data From Lille

    collection_name = dbname["stations_actuelles"]
    
    collection_lille = part1.get_lille()
    for station in collection_lille:
        
        formated = Donnees_station.formatt( station['fields']['nom'],
                                    geometry={'type': "Point", 'coordinates':station['fields']['geo']},
                                    ville="Lille",
                                    nb_place_total=station['fields']['nbplacesdispo'] + station['fields']['nbvelosdispo'],
                                    nb_place_dispo=station['fields']['nbplacesdispo'],
                                    nb_velo_dispo=station['fields']['nbvelosdispo'],
                                    date=time.asctime(time.gmtime())
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
                                    date=time.asctime(time.gmtime())
        )

        collection_name.insert_one(formated)
    print("données Lyon importées.")
    print("Les données des stations Vélib ont été importées avec succès")

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    maj_collection(dbname)

    