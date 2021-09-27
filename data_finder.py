import requests # module pour accéder aux APIs
import json # module pour travailler avec le format json


# =============================================================================
# get_lille permet de se connecter à l'API de Vélib de Lille et d'avoir les données associées
# renvoie les données des stations Vélib de Lille
def get_lille():
    url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

# =============================================================================
# get_lyon permet de se connecter à l'API de Vélib de Lyon et d'avoir les données associées
# renvoie les données des stations Vélib de Lyon
def get_lyon():
    url="http://api.citybik.es/v2/networks/velov"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])


# =============================================================================
# get_paris permet de se connecter à l'API de Vélib de Paris et d'avoir les données associées
# renvoie les données des stations Vélib de Paris
def get_paris():
    url="http://api.citybik.es/v2/networks/velib"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])


# =============================================================================
# get_rennes permet de se connecter à l'API de Vélib de Rennes et d'avoir les données associées
# renvoie les données des stations Vélib de Rennes
def get_rennes():
    url="http://api.citybik.es/v2/networks/le-velo-star"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("network", [])