# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:45:31 2021

@author: blond
"""

class Donnees_station:
    def __init__(self,nom="",geometry={type: "point",'coordinates':[0,0]},
                ville="",nb_place_total=0,nb_place_dispo=0,nb_velo_dispo=0,date=""):
        self.nom=nom
        self.geometry=geometry
        self.ville=ville
        self.nb_place_total=nb_place_total
        self.nb_place_dispo=nb_place_dispo
        self.nb_velo_dispo=nb_velo_dispo
        self.date=date
    