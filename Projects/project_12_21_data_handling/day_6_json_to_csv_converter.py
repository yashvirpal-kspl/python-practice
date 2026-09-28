import json
import csv
import os

INPUT_FILE = "movies.json"
OUTPUT_FILE = "converted_json_csv_data.csv"

def load_json_data(filename):
    if not os.path.exists(filename):
        print("Json file not found")
        return
    
    with open(filename,"r",encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            print("Invalid json format")
            

def convert_to_csv(data,output_file):
    if not data:
        print("No data to convert")
        return
    
    fieldname = list(data[0].keys())
    
    with open(output_file,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=fieldname)
        writer.writeheader()
        for record in data:
            writer.writerow(record)
            
        print(f"Converted {len(data)} records to {output_file}")  
        
        
def main():
    print("Converting json to csv....")
    data = load_json_data(INPUT_FILE)
    convert_to_csv(data,OUTPUT_FILE)
    
    
if __name__=="__main__":
    main()    
    
              
        
                
    


