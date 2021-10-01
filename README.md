mongoProject par Pierre Niclas et Corentin Blondeau

Programme en python pour manipuler une base de donnée sur MongoDB.
Les données concernent les stations Vélib de Lille, Rennes, Lyon et Paris.

Pour lancer le programme, exécuter le code de main.py .

Librairies python nécessaires : 
requests
json
pymongo
pymongo[srv]
ssl
time
datetime
threading
pprint
Pour les installer, excécuter la commande "pip install [librairie]" dans une console python.

Pour se connecter au serveur MongoDb, le programme utilise le lien : mongodb+srv://python:python@database1.fv5bh.mongodb.net/Database1?retryWrites=true&w=majority
Si vous voulez vous connecter au serveur MongoDb, utilisez le lien : mongodb+srv://user:user@database1.fv5bh.mongodb.net/test?authSource=admin&replicaSet=atlas-113114-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true

