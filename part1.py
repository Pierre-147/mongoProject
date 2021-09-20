import requests
import json


def get_lille():
    #fonction
    url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_lyon():

    url="http://api.citybik.es/v2/networks/velov"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])

def get_paris():
    #fonction mais changer de set de données
    url="http://api.citybik.es/v2/networks/velib"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])

def get_rennes():
    #fonctionne et dataset correct
    url="http://api.citybik.es/v2/networks/le-velo-star"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])