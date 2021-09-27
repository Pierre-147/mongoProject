# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:48:28 2021

@author: blond
"""

import pprint
import pymongo
import ssl

def get_database():
    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
    return client['Stations_Velib']

def near():
    print("Importer vos coordonnées : ")
    lat=int(input("lattitude : "))
    long=int(input("longitude : "))
    # Get the database
    dbname = get_database()
    query=[{
        '$geoNear': {
            'near': {
                'type': 'Point', 'coordinates': [lat,long]}, 
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
                'date', 'distance', '_id'
            ]
        }]
    liste_near=dbname['stations_actuelles'].aggregate(query)
    print("Résultats de la recherche :")
    for i in liste_near:
        pprint.pprint(i)

    
def recherche(name=''):
    if name=='':
        name=input("Donner le nom de la station (quelques lettres) : ")
    dbname = get_database()
    query = { "nom": { "$regex": name,"$options":"i" } }
    result = dbname['stations_actuelles'].find(query,{"_id":0,"date":0})
    print("Résultats de la recherche :")
    for i in result:
        pprint.pprint(i)


def update():
    recherche()
    name=input("Donner le nom complet de la station : ")
    item=input("Donner le champ à modifier : ")
    newvalue=input("Donner la nouvelle valeur du champs :")
    dbname = get_database()
    print(name,item,newvalue)
    dbname['stations_actuelles'].update_one({"nom": name}, {"$set": { item: newvalue}})
    print()
    recherche(name)


def supprimer():
    recherche()
    name=input("Donner le nom complet de la station : ")
    query = { "nom": { "$regex": name } }
    dbname = get_database()
    dbname['stations_actuelles'].delete_many(query)
    print("Station supprimée")


def supprimer_zone():
    coordonnees=[]
    for _ in range(4):
        print("Importez vos coordonnées : ")
        lat=int(input("lattitude : "))
        long=int(input("longitude : "))
        coordonnees.append([lat,long])
    coordonnees.append([coordonnees[0][0],coordonnees[0][1]])
    query={'geometry': {
        '$geoWithin': {
            '$geometry': {
                'type': 'Polygon', 
                'coordinates': [coordonnees]
                }
            }
        }
        }
    dbname = get_database()
    dbname['stations_actuelles'].delete_many(query)
    print("Stations de la zone supprimées")

def find_overused_station():
    query=[
            {
                '$project': {
                    '_id': {
                        'station_id': '$station_id', 
                        'dayOfWeek': {
                            '$dayOfWeek': '$date'
                        }, 
                        'hourOfDay': {
                            '$hour': '$date'
                        }, 
                        'averageBike': {
                            '$avg': '$nb_velo_dispo'
                        }, 
                        'totPlace': '$nb_place_total'
                    }
                }
            }, {
                '$match': {
                    '_id.dayOfWeek': {
                        '$in': [
                            2, 3, 4, 5, 6
                        ]
                    }, 
                    '_id.hourOfDay': 18
                }
            }, {
                '$addFields': {
                    'ratio': {
                        '$divide': [
                            '$_id.averageBike', '$_id.totPlace'
                        ]
                    }
                }
            }, {
                '$match': {
                    'ratio': {
                        '$lte': .2
                    }
                }
            }
        ]
    dbname = get_database()
    result=dbname['stations_actuelles'].aggregate(query)
    print("Résultats de la recherche :")
    for i in result:
        pprint.pprint(i)
