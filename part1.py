import requests
import json


def get_lille():
    url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    #pour retourner en format objet, enlever le s dans "loads"
    return response_json.get("records", [])


def get_lyon():
    url="https://download.data.grandlyon.com/ws/grandlyon/pvo_patrimoine_voirie.pvostationvelov/all.json?maxfeatures=-1&start=1"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    #pour retourner en format objet, enlever le s dans "loads"
    return response_json.get("records", [])
    
print (get_lyon())