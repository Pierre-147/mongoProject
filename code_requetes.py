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

def selection():
    fini=False
    query=[]
    while not fini:
        print("Sélection selon quel critère :")
        print("Ville : 1")
        print("Nom de station : 2")
        print("Coordonnées : 3")
        print("Nombre de places total : 4")
        print("Nombre de vélos disponible : 5")
        print("Nombre de places disponibles : 6")
        select='0'
        while select>'6' or select<'1':
            select=input()
        if select=='1':
            recherche=input('nom de la ville : ')
            print(recherche)
            query.append(
            {
                '$match': {
                    'villle': {
                        '$eq': recherche
                    }
                }
            })
        if select=='2':
            recherche=input('nom de la station : ')
            print(recherche)
            query.append(
            {
                '$match': {
                    'nom': {
                        '$eq': recherche
                    }
                }
            })
        if select=='3':
            longitude=input('Longitude : ')
            lattitude=input('Lattitude : ')
            print(longitude,lattitude) #############################
            query.append(
            {
                '$match': {
                    'villle': {
                        '$eq': recherche
                    }
                }
            })
        if select=='4':
            recherche=int(input('Nombre de places total : '))
            print(recherche)
            query.append(
            {
                '$match': {
                    'nb_place_total': {
                        '$eq': recherche
                    }
                }
            })
        if select=='5':
            recherche=int(input('Nombre de vélos disponible : '))
            print(recherche)
            query.append(
            {
                '$match': {
                    'nb_velo_dispo': {
                        '$eq': recherche
                    }
                }
            })
        if select=='6':
            recherche=int(input('Nombre de places disponible : '))
            print(recherche)
            query.append(
            {
                '$match': {
                    'nb_place_dispo': {
                        '$eq': recherche
                    }
                }
            })
        
        tempo=input("Avez-vous fini la sélection des critères ? O/N : ").upper()
        while tempo!='O' and tempo!='N':
            tempo=input()
        if tempo=='O':
            fini=True
        return query
    

def recherche():
    dbname = get_database()
    query=selection()
    query.append({
            '$unset': ['_id']
        })
    result = dbname['historique'].aggregate(query)
    print("Résultats de la recherche :")
    for i in result:
        pprint.pprint(i)

def update():
    dbname = get_database()
    query=selection()
    dbname['historique'].aggregate(query).update()#à faire

def delete():
    dbname = get_database()
    query=selection()
    dbname['historique'].delete_many(query)#à faire
    
if __name__ == "__main__":    
    delete()
    print('fin')
    prout=input()
    # coordonnees=[48,2]
    # near(coordonnees)
    #ratio()
    


