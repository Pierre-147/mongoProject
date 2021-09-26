"""
Created on Tue Sep 14 15:28:24 2021
@author: blond
"""

import time
import Donnees_station
import part1

def get_database():
    import pymongo
    import ssl



    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Vlib_Paris']
    

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    

    #Import data from Paris

    collection_name = dbname["Paris"]
    
    collection_paris = part1.get_paris()
    for station in collection_paris['stations']:
       
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Paris",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("Paris fini")


    #Import data from Rennes

    collection_name = dbname["Rennes"]
    
    collection_rennes = part1.get_rennes()
    for station in collection_rennes['stations']:

        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Rennes",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("Rennes fini")



    #Import data From Lille

    collection_name = dbname["Lille"]
    
    collection_lille = part1.get_lille()
    for station in collection_lille:
        
        formated = Donnees_station.formatt( station['fields']['nom'],
                                    geometry={'type': "point", 'coodinates':station['fields']['geo']},
                                    ville="Lille",
                                    nb_place_total=station['fields']['nbplacesdispo'] + station['fields']['nbvelosdispo'],
                                    nb_place_dispo=station['fields']['nbplacesdispo'],
                                    nb_velo_dispo=station['fields']['nbvelosdispo'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("Lille fini")


    #Import data From Lyon

    collection_name = dbname["Lyon"]
    
    collection_lyon = part1.get_lyon()
    for station in collection_lyon['stations']:
        
        formated = Donnees_station.formatt( station['name'],
                                    geometry={'type': "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Lyon",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bikes'],
                                    date=time.asctime(time.localtime())
        )

        collection_name.insert_one(formated)
    print("Lyon fini")