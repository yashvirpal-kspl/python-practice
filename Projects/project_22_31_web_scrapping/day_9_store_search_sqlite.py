import os 
import csv
from datetime import datetime
import requests
import schedule
import time
import sqlite3

API_URL="https://api.coingecko.com/api/v3/coins/markets"

PARAMAS = {
    'vs_currency':'usd',
    'order':'market_cap_desc',
    'per_page':10,
    'page':1,
    'sparkline':False
}

DB_NAME = "crypto.db"


def fetch_crypto_data():
    response = requests.get(API_URL,params=PARAMAS)
    return response.json()

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS crypto_prices(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp TEXT,
                       coin TEXT,
                       price REAL
                   )
                   
                   ''')
    conn.commit()
    conn.close()
    
def save_to_database(data):
    conn = sqlite3.connect(DB_NAME)
    cursur = conn.cursor()   
    
    timestamp = datetime.now().strftime("%y-%m-%d %H-%M-%S")
    for coin in data:
        cursur.execute('''
                       INSERT INTO crypto_prices (timestamp,coin,price)
                       VALUES (?,?,?)
                       
                       ''',(timestamp,coin['id'],coin['current_price']))
    
    conn.commit()
    conn.close() 
    print("Price saved to database")
    
def search_coin(coin_name):
    conn = sqlite3.connect(DB_NAME)
    cursur = conn.cursor()   
        
    timestamp = datetime.now().strftime("%y-%m-%d %H-%M-%S")
        
    cursur.execute('''
           SELECT * FROM crypto_prices 
           where coin = ? 
           order by timestamp DESC 
           limit 1 
            
            ''',(coin_name,))
    result = cursur.fetchone()
    conn.close()
    
    print("Result RAW",result) 
    
    if result:
        print(f"${result[3]}")
    
          
 
    
    
def main():
    create_table()
    
    print("1. Fetch and Store Crypto Data")
    print("2. Search latest price of the coin")
    #print("3. Exit")
    
    choice = input("Choose an option: ").strip()
    
    if choice =="1":
        data = fetch_crypto_data()
        save_to_database(data)
    elif choice == "2":
            searchcoin = input("Enter the coin name: ").strip().lower()
            search_coin(searchcoin)
    else:
        print("Invalid Option")        
        
        
if __name__ == "__main__":
    main()   