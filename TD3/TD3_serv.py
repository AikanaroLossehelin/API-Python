# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 12:47:47 2023

@author: aikan
"""

import multiprocessing
import crypto_data_server
import crypto_data_extract

def main():
    # Crée un espace de mémoire partagée
    shm = multiprocessing.shared_memory.SharedMemory(create=True, size=2048 * 2048)
    lock = multiprocessing.Lock()

    # Récupère les données dans le processus data_process
    data_process = multiprocessing.Process(target=crypto_data_extract.main, args=(shm, lock))
    data_process.start()

    # Démarre le serveur socket
    crypto_data_server.run(shm, lock)

    # Attend que le processus de récupération des données se termine 
    data_process.join()

if __name__ == "__main__":
    main()
