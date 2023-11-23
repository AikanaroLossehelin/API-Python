# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 11:56:58 2023

@author: aikan
"""
import requests
import time
import json
from datetime import datetime, timedelta
from multiprocessing import shared_memory, Lock


###############################################################################
#
# Data Extraction Function
#
###############################################################################

# Récupère les données OHLCV pour une paire de cryptomonnaies
def get_info(pair, interval, limit=1000):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': pair,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
    
###############################################################################
#
# Shared Memory Management Functions
#
###############################################################################

# Lit et désérialise les données de la mémoire partagée.
def read_shared_memory(shm, lock):
    with lock:
        data = shm.buf.tobytes().split(b'\0', 1)[0]
    return json.loads(data)


# Met à jour la mémoire partagée avec les nouvelles données tout en conservant les données des dernières 24 heures.
def update_shared_memory(shm, new_data, lock):
    with lock:
        # Lit les données actuelles si possible sinon initialise à vide en cas d'échec
        try:
            current_data = json.loads(shm.buf.tobytes().split(b'\0', 1)[0])
        except json.JSONDecodeError:
            current_data = {}

        # Met à jour et filtre les données pour chaque paire
        for pair, klines in new_data.items():
            if pair in current_data:
                # Concatène les anciennes et nouvelles données
                merged_data = current_data[pair] + klines
                # Elimine les données au-delà des dernières 24h
                cutoff_time = datetime.now() - timedelta(days=1)
                filtered_data = [kline for kline in merged_data if datetime.fromtimestamp(kline[0]/1000) > cutoff_time]
                current_data[pair] = filtered_data
            else:
                current_data[pair] = klines
        
        # Écriture des données mises à jour dans la mémoire partagée
        serialized_data = json.dumps(current_data).encode('utf-8')
        shm.buf[:len(serialized_data)] = serialized_data
        shm.buf[len(serialized_data)] = 0  # Marqueur de fin        
        
###############################################################################
#
# Main Function
#
###############################################################################

# Donne le rapport de conversion à l'heure de l'unité temps s
def convert_time_unit(s):
    return (s=='s')*3600 + (s=='m')*60 + (s=='h') + (s=='d')/24 + (s=='w')/(7*24) + (s=='M')/(30.5*24)
    

def main(shm, lock, pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "XRPUSDT"], interval = '15m'):
    unit = convert_time_unit(interval[-1:])
    nb_data = int(24*unit/int(interval[:-1])) # Nombre de bougies dans les 24 dernières heures
    
    try:
        while True:
            market_data = {}
            for pair in pairs:
                data = get_info(pair, interval)
                if data:
                    market_data[pair] = data[-nb_data:]  # Stocke les entrées des dernières 24h
                else:
                    print(f"Impossible de récupérer les données de la paire {pair}")

            update_shared_memory(shm, market_data, lock)
            # Vérifie que la mémoire partagée contient les bonnes données
            # print(read_shared_memory(shm, lock))

            time.sleep(60)
    finally:
        shm.close()
        shm.unlink()  # Nettoye la mémoire partagée à la fin du programme


# Cette condition empêche l'exécution du code lors de l'importation du module
if __name__ == "__main__":
    # Créer un espace de mémoire partagée
    shm = shared_memory.SharedMemory(create=True, size=2048 * 2048)
    lock = Lock()
    main(shm, lock)
