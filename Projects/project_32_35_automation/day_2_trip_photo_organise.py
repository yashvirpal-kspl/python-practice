import os

def batch_rename(folder,base_name,extenstion):
    files = [f for f in os.listdir(folder) if f.lower().endswith(extenstion.lower())]
    
    files.sort()
    
    if not files:
        print("No files found in dir")
        return 
    for i,file in enumerate(files,start=1):
        new_name = f"{base_name}_{i}{extenstion}"
        
        print(f"{file} =>{new_name}")
        
    confirm = input("Press (y) to confirm or (n) to reject: ").strip().lower()  
    if confirm !='y':
        print("Canceled")
        return
    
    for i, file in enumerate(files,start=1):
        src = os.path.join(folder,file)  
        new_name = f"{base_name}_{i}{extenstion}"
        dest = os.path.join(folder,new_name) 
        os.rename(src,dest)
        
    print(f"Renamed {len(files)} files successfully")    

if __name__ == "__main__":
    folder = input("Enter folder path or leave blank for current folder: ").strip() or os.getcwd()
    
    if not os.path.isdir(folder):
        print("Invalid folder")
    else:
        base_name = input("Enter base name for file: ").strip()    
        extenstion = input("Enter extenstion name for file: ").strip()    
        
        batch_rename(folder,base_name,extenstion)