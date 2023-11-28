# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:46:49 2023

@author: aikan
"""

import requests

#Fonction de nettoyage pour l'affichage des données
def clean(data):
    if not data is None:
        return data[0]
    return data

#Fonction de récupération du token d'authentification de l'utilisateur
def get_jwt_token(username, password, BASE_URL):
    auth_url = f"{BASE_URL}/token"
    response = requests.post(auth_url, data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Erreur:", response.status_code, response.text)
        raise ValueError("Authentification échouée")
        
        
#Fonction pour mettre à jour la licence de l'utilisateur
def update_user_licence(token, new_licence, BASE_URL):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/user/licence"
    data = {"licence": new_licence}
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la mise à jour de la licence:", response.status_code, response.text)
        return None
    

#Fonction pour obtenir la licence de l'utilisateur
def get_user_licence(token, BASE_URL):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/user/licence", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération de la licence:", response.status_code, response.text)
        return None
 
    
#Fonction pour obtenir les données d'un indicateur financier
def get_indicator_data(endpoint, token, BASE_URL):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur:", response.status_code, response.text)
        return None


#Fonction pour obtenir les données d'une monnaie
def get_coin_data(endpoint, BASE_URL, name=None):
    url = f"{BASE_URL}/{endpoint}"
    if name:
        url += f"?name={name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur:", response.status_code, response.text)
        return None

