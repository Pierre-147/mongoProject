# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:28:24 2021

@author: blond
"""

import part1

def get_database():
    import pymongo
    import ssl

    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    return client['Vlib_Paris']
    

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    
    collection_name = dbname["Paris"]
    
    collection_paris = part1.get_paris()
    for station in collection_paris:
         collection_name.insert_many([station])

    """   
    collection_2 = dbname["Rennes"]
    
    collection_rennes = part1.get_rennes()
    for station in collection_rennes:
        collection_2.insert_many([station])

    collection_2 = dbname["Lille"]
    
    collection_lille = part1.get_lille()
    for station in collection_lille:
        collection_2.insert_many([station])
    



    collection_2 = dbname["Lyon"]
    
    collection_lyon = part1.get_lyon()
    for station in collection_lyon:
        collection_2.insert_many([station])

   """