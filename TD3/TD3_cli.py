# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:52:56 2023

@author: aikan

Adresse serveur bis : '127.0.0.1'
Port de test bis : 65432
"""

import socket
import json
import time

def request_pair_data(pair):
    HOST = 'localhost' # L'adresse du serveur
    PORT = 6789        # Le port utilisé par le serveur
    request_data = json.dumps({"pair": pair})  # Création de la requête JSON

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request_data.encode('utf-8'))
        
        response = s.recv(2048)  # Attend la réponse serveur
        print(f"Données reçues: {response.decode('utf-8')}")
        time.sleep(1)

if __name__ == "__main__":
    request_pair_data("ETHUSDT")