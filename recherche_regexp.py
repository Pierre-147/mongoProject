import pymongo

def search(name, collection):
    query = { "nom": { "$regex": name } }
    res = collection.find(query)
    return res

def search(name, collection):
    query = { "nom": { "$regex": name } }
    collection.delet_many(query)

def update(name, item, newvalue, collection):
    collection.update_one({"nom": name}, {"$set": { item: newvalue}})