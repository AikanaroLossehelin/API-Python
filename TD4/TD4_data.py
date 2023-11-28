# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 20:25:26 2023

@author: aikan
"""
from typing import Literal
from pydantic import BaseModel, Field

#Modèle de notre utilisateur avec ses attributs
class User(BaseModel):
    nom: str
    prenom: str
    pseudo: str
    email: str
    password: str
    disabled: bool = False
    licence: Literal["étudiant", "premium", "entreprise"]

class UserInDB(User):
    hashed_password: str

#Modèle de licence que peuvent détourner les utilisateurs avec possibilité de modifier sa valeur
class LicenceUpdate(BaseModel):
    licence: Literal["étudiant", "premium", "entreprise"] = Field(..., description="Nouvelle licence de l'utilisateur")

#Données de nos utilisateurs
users = [
    {
        "nom": "Dupont",
        "prenom": "Jean",
        "pseudo": "jdupont",
        "email": "jean.dupont@example.com",
        "password" : "password_1",
        "disabled": False,
        "licence": "entreprise"
    },
    {
        "nom": "Martin",
        "prenom": "Alice",
        "pseudo": "amartin",
        "email": "alice.martin@example.com",
        "password" : "password_2",
        "disabled": False,
        "licence": "étudiant"
    },
    {
        "nom": "Leroy",
        "prenom": "Émile",
        "pseudo": "eleroy",
        "email": "emile.leroy@example.com",
        "password" : "password_3",
        "disabled": True,
        "licence": "premium"
    },
    {
        "nom": "Leprince",
        "prenom": "Albert",
        "pseudo": "aleprince",
        "email": "albert.leprince@example.com",
        "password" : "password_4",
        "disabled": False,
        "licence": "premium"
    },
    {
        "nom": "Duchou",
        "prenom": "Julien",
        "pseudo": "jduchou",
        "email": "julien.duchou@example.com",
        "password" : "password_5",
        "disabled": False,
        "licence": "premium"
    },
    {
        "nom": "Soleau",
        "prenom": "Hugo",
        "pseudo": "hsoleau",
        "email": "hugo.soleau@example.com",
        "password" : "password_6",
        "disabled": False,
        "licence": "entreprise"
    }
]

#Données des monnaies
coins = {"coin" : [{"name": "BTC",
         "symbol" : "btc"},
         {"name": "ETH",
          "symbol" : "eth"},
         {"name": "ADA",
          "symbol" : "ada"},
         {"name": "USD",
          "symbol" : "usd"}]
    }

#Données de test variées
indicators = {
    "coins": ["BTC", "ETH", "ADA", "USD"],
    "RSI": [{
        "value": 42.7,
        "date": "2023-11-23",
        "crypto": "BTC"
    },
        {"value": 35.6,
        "date": "2023-12-23",
        "crypto": "BTC"},
        {"value": 37.9,
        "date": "2023-11-23",
        "crypto": "ETH"}],
    
    "MACD": [{
        "value": 0.0045,
        "date": "2023-12-23",
        "crypto": "ETH"
    },
        {
            "value": 0.0035,
            "date": "2023-10-23",
            "crypto": "BTC"
        },
        {
            "value": 0.0026,
            "date": "2023-11-23",
            "crypto": "ETH"
        }]
}

