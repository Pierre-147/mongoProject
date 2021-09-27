import pprint   #module pour la présentation des resultats
import pymongo  #module pour utiliseer mongodb
import ssl      #module pour se connecter au serveurs mongodb

def get_database():
    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
    return client['Stations_Velib']

# =============================================================================
# near cherche les trois stations les plus proches des coordonées indiquez et renvoie
# leur nom, ville, nombre de vélo et de places disponibles

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

# =============================================================================
# recherche renvoie toute les stations dont le nom contient les  carachteres indiquez
# sans se soucier de la capitalisation
    
def recherche(name=''):
    if name=='':
        name=input("Donner le nom de la station (quelques lettres) : ")
    dbname = get_database()
    query = { "nom": { "$regex": name,"$options":"i" } }
    result = dbname['stations_actuelles'].find(query,{"_id":0,"date":0})
    print("Résultats de la recherche :")
    for i in result:
        pprint.pprint(i)

# =============================================================================
# update permet de modifier un des elements d'une station dont il faut indiquer le nom entier

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


# =============================================================================
# supprimer permet de supprimer toutes les information d'une station dont on indique le nom exacte

def supprimer():
    recherche()
    name=input("Donner le nom complet de la station : ")
    query = { "nom": { "$regex": name } }
    dbname = get_database()
    dbname['stations_actuelles'].delete_many(query)
    print("Station supprimée")

# =============================================================================
# supprime_zones permet de selectioner toutes stations dans un rectangle dont on fournit les coins
# et les supprime toutes

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

# =============================================================================
# find_overused_station selectione toutes les données de l'historique provenant d'un jour de la semaine
# et ayant ete obtenue entre 18h et 19h, calcul le ratio de velos disponible par rapport à la taille de la station
# puis renvoie celles dont le ratio est inférieur a 0.2

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
