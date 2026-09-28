#weather_response = "https://api.openweathermap.org/data/4.0/onecall/current?lat={lat}&lon={lon}&appid={API key}"
#geo_responce = "http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}"

import os 
import csv
from datetime import datetime
import requests

FILENAME = "weather_logs.csv"
API_KEY = "Opean weather api"

if not os.path.exists(FILENAME):
    with open(FILENAME,"w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date","City","Temperature","Condition"])
        
        
def log_weather():
    city = input("Enter Your City: ").strip().lower()
    date = datetime.now().strftime("%y-%m-%d")
    
    with open(FILENAME,"r",newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            if row["Date"] ==date and row["City"].lower() == city:
                print("Entry for this city and date exist")
                return
    
    try:
        
        weather_url = f"https://api.openweathermap.org/data/2.5/weather/?q={city}&appid={API_KEY}"
      
       # print(geo_url)
        geo_responce = requests.get(weather_url)
        data = geo_responce.json()
        print("GEO Respose",data)
        
        if geo_responce.status_code != 200:
            #print(f"API Error {data.get("message")}")
            print(f"API Error !")
            
        temp = data["main"]["temp"] 
        condition = data["weather"][0]["main"]   
        
        with open(FILENAME,"a",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date,city.title(),temp,condition])
                print(f"Logged: {temp} {condition} in {city.title()} on {date}")
        
    except Exception as e:
        print("Failed to make API call")
    

def view_log():
    with open(FILENAME,"r",newline="",encoding="utf-8") as f:
        reader = list(csv.reader(f))
        
        if len(reader) <=1:
            print("No Entries")
            
        for row in reader[1:]:
            print(f"{row[0]} : {row[1]} : {row[2]} : {row[3]}")        

def main():
    while True:
        print("Realtime Weather logger")
        print("1. Add Weather logger")
        print("2. View Weather logger")
        print("3. exit")
        
        choice = input("Choose an option: ").strip()
        
        match choice:
            case "1": log_weather()
            case "2": view_log()
            case "3": break
            case _: print("Invalid Choice")
            
if __name__ == "__main__":
    main()            
            


