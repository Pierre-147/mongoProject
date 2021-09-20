# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:28:24 2021

@author: blond
"""

import time
from Donnees_station import Donnees_station
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
       
        formated = Donnees_station( station['name'],
                                    geometry={type: "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Paris",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bike'],
                                    date=time.time()
        )

        collection_name.insert_many([formated])


    #Import data from Rennes

    collection_2 = dbname["Rennes"]
    
    collection_rennes = part1.get_rennes()
    for station in collection_rennes['stations']:

        formated = Donnees_station( station['name'],
                                    geometry={type: "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Rennes",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bike'],
                                    date=time.time()
        )

        collection_name.insert_many([formated])



    #Import data From Lille

    collection_2 = dbname["Lille"]
    
    collection_lille = part1.get_lille()
    for station in collection_lille:
        
        formated = Donnees_station( station['fields']['nom'],
                                    geometry={type: "point", 'coodinates':station['fields']['geo']},
                                    ville="Lille",
                                    nb_place_total=station['fields']['nbplacesdispo'] + station['fields']['nvelosdispo'],
                                    nb_place_dispo=station['fields']['nbplacesdispo'],
                                    nb_velo_dispo=station['fields']['nvelosdispo'],
                                    date=time.time()
        )

        collection_name.insert_many([formated])
        


    #Import data From Lyon

    collection_2 = dbname["Lyon"]
    
    collection_lyon = part1.get_lyon()
    for station in collection_lyon['stations']:
        
        formated = Donnees_station( station['name'],
                                    geometry={type: "point", 'coodinates':[station['latitude'],station['longitude']]},
                                    ville="Lyon",
                                    nb_place_total=station['extra']['slots'],
                                    nb_place_dispo=station['empty_slots'],
                                    nb_velo_dispo=station['free_bike'],
                                    date=time.time()
        )

        collection_name.insert_many([formated])
