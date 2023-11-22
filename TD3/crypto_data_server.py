# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 12:46:51 2023

@author: aikan

Adresse locale bis : '127.0.0.1'
Port de test bis : 65432
"""
import socket
import json
import time
from multiprocessing import shared_memory, Lock

def read_shared_memory(shm, lock):
    # Lit et désérialise les données de la mémoire partagée
    with lock:
        data = shm.buf.tobytes().split(b'\0', 1)[0]
        return json.loads(data) if data else {}

def run(shm, lock):
    HOST = 'localhost'  # Adresse locale
    PORT = 6789         # Port à utiliser

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Ecoute serveur sur {HOST}:{PORT}")

        while True:
            try:
                conn, addr = s.accept()
                print(f"Connecté à l'adresse : {addr}")

                with conn:
                    data = conn.recv(2048)
                    if not data:
                        print("Pas de données reçues. Fermeture des connexions.")
                        break

                    try:
                        request = json.loads(data.decode('utf-8'))
                        print(f"Requête reçue: {request}")
                        pair = request.get("pair")
                    except json.JSONDecodeError:
                        response = "Invalid JSON format"
                        conn.sendall(response.encode('utf-8'))
                        print("Objet JSON reçu de format incorrect.")
                        continue

                    market_data = read_shared_memory(shm, lock)
                    if pair and pair in market_data:
                        response = json.dumps(market_data[pair])
                    else:
                        response = f"No data available for {pair}"

                    conn.sendall(response.encode('utf-8'))
                    time.sleep(1)  # Donner un peu de temps avant de fermer la connexion

            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            


if __name__ == "__main__":
    run()