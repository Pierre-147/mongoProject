import pymongo

def search(name, collection):
    query = { "nom": { "$regex": name } }
    res = collection.find(query)
    return res