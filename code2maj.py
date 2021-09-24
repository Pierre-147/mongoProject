# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:48:28 2021

@author: blond
"""

import part1
import codeprojet
import pprint
import pymongo
import ssl
import time

def get_database():

    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Stations_Velib']
    
def history_data():
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
    codeprojet.maj_collection(dbname)

def near(coordonnees):
    # Get the database
    dbname = get_database()
    query=[{
        '$geoNear': {
            'near': {
                'type': 'Point', 'coordinates': coordonnees}, 
            'distanceField': 'distance', 
            'query': {}
            }
        }, {
        '$sort': {
            'distance': 1
        }
    }, {
        '$limit': 3
    },{
            '$unset': [
                'date', 'geometry', '_id'
            ]
        }]
    liste_near=dbname['stations_actuelles'].aggregate(query)
    for i in liste_near:
        pprint.pprint(i)

def ratio():
    dbname = get_database()
    query=[
        {
            '$match': {
                'nb_place_total': {
                    '$gt': 0
                }
            }
        }, {
            '$addFields': {
                'ratio': {
                    '$divide': [
                        '$nb_velo_dispo', '$nb_place_total'
                    ]
                }
            }
        }, {
            '$match': {
                'ratio': {
                    '$lte': 0.2
                }
            }
        },{
            '$unset': [
                'date', 'geometry', '_id','ratio'
            ]
        }
       ]
    result = dbname['historique'].aggregate(query)
    print("Résultats de la recherche :")
    for i in result:
        pprint.pprint(i)

def admin_programme():
    select=input("Selection de mode")
    if select==1:#search
        a=1
    elif select==2:#update
        a=2

if __name__ == "__main__":    
    history_data()
    
     # coordonnees=[48,2]
     # near(coordonnees)
    #ratio()
    


