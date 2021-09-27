import database_manager # code pour travailler la base de données
import code_requetes

if __name__ == "__main__":
    print("Que voulez-vous faire?")
    print("Initialiser la base de données : 1")
    print("Lancer un programme automatique d'actualisation et d'historisation des données : 2")
    print("Avoir les stations proches de vos coordonnées : 3")
    print("Rechercher une station : 4")
    print("Mettre à jour une station : 5")
    print("Supprimer des stations : 6")
    print("Désactiver les stations d'une zone : 7")
    print("Avoir toutes les stations avec un ratio d'occupation de 20% ou moins : 8")
    choix='0'
    while choix>'8' or choix<'1':
        choix=input()
    if choix =="1":
        database_manager.initialisation()
    if choix=="2":
        database_manager.historisation()
    if choix=='3':
        code_requetes.near()
    if choix=='4':
        code_requetes.recherche()
    if choix=='5':
        code_requetes.update()
    if choix=='6':
        code_requetes.supprimer()
    if choix=='7':
        code_requetes.supprimer_zone()
    if choix=='8':
        code_requetes.find_overused_station()
    

