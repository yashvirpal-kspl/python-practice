import os 
import csv
from datetime import datetime
import requests
import schedule
import time
API_URL="https://api.coingecko.com/api/v3/coins/markets"

PARAMAS = {
    'vs_currency':'usd',
    'order':'market_cap_desc',
    'per_page':10,
    'page':1,
    'sparkline':False
}

CSV_FILE = 'crypto_prices.csv'

def fetch_crypto_data():
    response = requests.get(API_URL,params=PARAMAS)
    return response.json()
def save_to_csv(data):
    file_exist = os.path.isfile(CSV_FILE)  # return true and false
    
    with open(CSV_FILE,'a',newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exist:
            writer.writerow(['timestamp','coin','price'])
        
        timestamp = datetime.now().strftime("%y-%m-%d %H-%M-%S")   
        
        for coin in data:
            writer.writerow([timestamp,coin['id'],coin['current_price']]) 
            
        print("✅ Data save to csv")   
        
def job():
    print("fetching data hourly ......")
    crypto_data = fetch_crypto_data()
    save_to_csv(crypto_data)
    
#schedule.every().day.at("10:30").do(job)    
schedule.every().hour.at(":00").do(job)  
while True:
    schedule.run_pending()
    time.sleep(1)  
    
def main():
    print("Fetching live crypto data....")
    crypto_data = fetch_crypto_data()
    
    save_to_csv(crypto_data)
    print("*" * 30)
    for coin in crypto_data:
        print(f"{coin['id']}-${coin['current_price']}")  
    print("*" * 30)
    
    choice = input("enter the coin to get graph: ").strip().lower()                
    
    if choice:
        plot_graph(choice)
        
        
if __name__ == "__main__":
    main()   