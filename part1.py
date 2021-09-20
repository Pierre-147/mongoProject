import requests
import json


def get_lille():
    url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_lyon():
    url="https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

def get_paris():
    #fonction mais changer de set de données
    url="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("data", [])

def get_rennes():
    url="https://data.rennesmetropole.fr/explore/dataset/etat-des-stations-le-velo-star-en-temps-reel/download?format=json"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json


