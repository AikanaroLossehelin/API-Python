# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 15:11:11 2023

@author: aikan
"""

import requests
import pandas as pd


def get_details(coin_id) :
    
    detailed_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    detailed_response = requests.get(detailed_url)
    return detailed_response.json()


def get_volume(coin_id) :

   coin_details = get_details(coin_id)
   if 'market_data' in coin_details:
        coin_details = coin_details['market_data']['total_volume']
        coin_dict = {"id": list(coin_details.keys()), "volume": list(coin_details.values())}
        return pd.DataFrame(coin_dict)
   else:
        return pd.DataFrame(columns=["id", "volume"])


def pick_volume(coin_id, coin):
    
    temp_coin = get_volume(coin_id)
    volume = temp_coin.loc[temp_coin['id'] == coin, 'volume']
    if volume.empty :
        return 0
    else :
        return volume.iloc[0]
    
    
def sort_coin_vs_crypt(df_coin, threshold) :
    ndf_coin = pd.DataFrame(0, index=df_coin.index, columns=["id", "name", "volume", "currency"])
    
    for index, row in df_coin.iterrows() :
        coin_id = row['id']
        ndf_coin.at[index, 'id'] = coin_id
        ndf_coin.at[index, 'name'] = row['name']
        
        vol_btc = pick_volume(coin_id, 'btc')
        vol_eth = pick_volume(coin_id, 'eth')
        
        if vol_btc > vol_eth :
            ndf_coin.at[index, 'volume'] = vol_btc
            ndf_coin.at[index, 'currency'] = 'btc'
        else:
            ndf_coin.at[index, 'volume'] = vol_eth
            ndf_coin.at[index, 'currency'] = 'eth'
    
    ndf_coin = ndf_coin.sort_values(by='volume', ascending=False)
    ndf_coin = ndf_coin.reset_index(drop=True)

    ndf_coin = ndf_coin.iloc[:threshold]
    
    return ndf_coin


def sort_coin_vs_curr(df_curr, threshold) :
    ndf_curr = pd.DataFrame(0, index=df_curr.index, columns=["id", "name", "volume_usd", "volume_usdc", "volume_tusd", "max_volume"])
    
    for index, row in df_curr.iterrows() :
        curr_id = row['id']
        ndf_curr.at[index, 'id'] = curr_id
        ndf_curr.at[index, 'name'] = row['name']
        
        vol_usd = pick_volume(curr_id, 'usd')
        vol_usdc = pick_volume(curr_id, 'eth')
        vol_tusd = pick_volume(curr_id, 'tusd')
        
        ndf_curr.at[index, 'volume_usd'] = vol_usd
        ndf_curr.at[index, 'volume_usdc'] = vol_usdc
        ndf_curr.at[index, 'volume_tusd'] = vol_tusd
        ndf_curr.at[index, 'max_volume'] = max(vol_usd, vol_usdc, vol_tusd)
    
    ndf_curr = ndf_curr.sort_values(by='max_volume', ascending=False)
    ndf_curr = ndf_curr.reset_index(drop=True)

    ndf_curr = ndf_curr.iloc[:threshold]
    
    return ndf_curr


def print_info(list_coin) :
    
    for index, row in list_coin.iterrows() :
        
        coin_id = row['id']
        coin_details = get_details(coin_id)
        
        # Imprimer des informations clés
        print(coin_details['name'])
        if 'usd' in coin_details['market_data']['current_price'] :
            print("Valeur USD :", coin_details['market_data']['current_price']['usd'], "USD")
        if 'eur' in coin_details['market_data']['current_price'] :    
            print("Valeur EUR :", coin_details['market_data']['current_price']['eur'], "EUR")
        if 'eth' in coin_details['market_data']['current_price'] :
            print("Valeur USDC :", coin_details['market_data']['current_price']['eth'], "USDC")
        if 'usdt' in coin_details['market_data']['current_price'] :
            print("Valeur USDC :", coin_details['market_data']['current_price']['usdt'], "USDT")
        print("Volume :", coin_details['market_data']['total_volume']['usd'], "USD")


def print_coin_vs_crypt(df_coin) :
    
    ndf_coin = sort_coin_vs_crypt(df_coin, 3)    
    i=1
    
    for index, row in ndf_coin.iterrows():
        name = row['name']
        coin_id = row['id']
        symbol = df_coin.loc[df_coin['id'] == coin_id, 'symbol'].iloc[0]
        volume = row['volume']
        currency = row['currency']
        
        print(f"{i}. {name} : {volume} {symbol}/{currency}")
        
        i+=1
    del ndf_coin


def print_coin_vs_curr(df_curr):
    
    ndf_curr = sort_coin_vs_curr(df_curr, 3)
    i = 1
    
    for index, row in ndf_curr.iterrows():
        name = row['name']
        curr_id = row['id']
        symbol = df_curr.loc[df_curr['id'] == curr_id, 'symbol'].iloc[0]
        volume_usd = row['volume_usd']
        volume_usdc = row['volume_usdc']
        volume_tusd = row['volume_tusd']
        
        print(f"{index+1}. {name} : {volume_usd} {symbol}/USD, {volume_usdc} {symbol}/USDC, {volume_tusd} {symbol}/TUSD")
        
        i+=1
    del ndf_curr


def execute_ex(n) :
    
    if n == 1:
        list_coin = pd.DataFrame({'id' : ["bitcoin", "ethereum"]})
        
        print("") ; print("Exercice 1") ; print("")

        print_info(list_coin)
    
    else :
        url_tick = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        response_tick = requests.get(url_tick)
        cryptcoin = response_tick.json()
        
        df_coin_speed = pd.DataFrame(cryptcoin)
        df_coin_speed = df_coin_speed[["id", "symbol", "name"]]
        
        if n == 2 :
            
            
            df_tick = pd.DataFrame(cryptcoin[:10])

            print("") ; print("Exercice 2") ; print("")
            
            list_coin_2 = df_tick[['id']]
            
            print_info(list_coin_2)
        
        if n == 3:
            
            print("") ; print("Exercice 3") ; print("")
            
            print_coin_vs_crypt(df_coin_speed)
        
        if n == 4 :
            
            print("") ; print("Exercice 4") ; print("")
            
            print_coin_vs_curr(df_coin_speed)
            
###############################################################################
################################### MAIN ######################################
###############################################################################

        
if __name__ == '__main__' :
    """
    url_coin = "https://api.coingecko.com/api/v3/coins"
    """
    
    ########################### EXERCICE 1 ####################################
    
    execute_ex(1)
    
    ########################### EXERCICE 2 ####################################
    
    execute_ex(2)
    
    ########################### EXERCICE 3 ####################################
    
    execute_ex(3)
    
    ########################### EXERCICE 4 ####################################
    
    execute_ex(4)
        
    ########################### EXERCICE 5 ####################################
    
    """
    Nous avons choisi d'utiliser les données de marché car elles sont plus complètes et permet 
    d'accéder aux différentes valeurs à des périodes différentes. Ici nous avons choisi de traiter
    les seules données historiques des dernières 24h afin de pouvoir éventuellement effectuer un 
    suivi journalier des volumes échangés en les stockant dans un fichier.
    """
    
