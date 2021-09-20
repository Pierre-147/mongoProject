# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:28:24 2021

@author: blond
"""


def get_database():
    import pymongo
    import ssl

    client = pymongo.MongoClient("mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs=ssl.CERT_NONE)

    
    return client['user_shopping_list']
    

if __name__ == "__main__":    
    
    # Get the database
    dbname = get_database()
    
    collection_name = dbname["user_1_items"]
    
    item_1 = {
    "item_name" : "Blender",
    "max_discount" : "10%",
    "price" : 340,
    "category" : "kitchen appliance"
    }
    
    item_2 = {
    "item_name" : "Egg",
    "category" : "food",
    "price" : 36,
    }
    print(item_1)
    collection_name.insert_many([item_1,item_2])
    
    
    