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
    print("Importer vos coordonnées : ")
    lat=int(input("lattitude : "))
    long=int(input("longitude : "))
    # coordo
    # find({'geometry': {
    # $geoWithin: {
    # "$geometry": {
    # "type": "Polygon",
    # "coordinates": [ ….] }

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

