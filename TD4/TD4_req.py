# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:27:26 2023

@author: aikan
"""

from TD4_cli import *

if __name__ == '__main__' :

    BASE_URL = "http://localhost:8000"
    
    username = "amartin"
    password = "password_2"

    # Obtenir le JWT token
    token = get_jwt_token(username, password, BASE_URL)

    #user_licence = get_user_licence(token, BASE_URL)
    #print("Licence de l'utilisateur:", user_licence)

    #licence_update_response = update_user_licence(token, "entreprise", BASE_URL)
    #print("Réponse de la mise à jour de la licence:", licence_update_response)

    user_licence = get_user_licence(token, BASE_URL)
    print("Licence de l'utilisateur:", user_licence)
    
    coin_data = get_coin_data("coins/coin", BASE_URL)
    print("Coins Data:", clean(coin_data))
    
    #Obtenir les données RSI
    rsi_data = get_indicator_data("indicators/rsi", token, BASE_URL)
    print("RSI Data:", clean(rsi_data))

    #Obtenir les données MACD
    macd_data = get_indicator_data("indicators/macd", token, BASE_URL)
    print("MACD Data:", clean(macd_data))
    
    #Accès public aux données d'un coin ETH
    eth_coin_data = get_coin_data("coins/coin", BASE_URL, name="ETH")
    print("ETH Coin Data:", clean(eth_coin_data))
    
    