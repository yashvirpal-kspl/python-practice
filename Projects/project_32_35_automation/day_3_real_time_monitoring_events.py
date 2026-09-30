import os 
import shutil

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

WATCH_FOLDER = os.path.expanduser("Images")

FILE_DESTS = {
    '.pdf':"PDFs",
    '.jpg':"Images",
    '.png':"Images",
}


class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("ON_Created Event=>",event)
        #return super().on_created(event)
        if event.is_directory:
            return
        
        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()
        
        dest_folder = FILE_DESTS.get(ext,'Others')
        full_dest = os.path.join(WATCH_FOLDER,dest_folder)
        
        os.makedirs(full_dest,exist_ok=True)
        
        move_to = os.path.join(full_dest,os.path.basename(filepath))
        try:
            
            shutil.move(filepath,move_to)
            print(f"Move from {filepath} to {move_to}")
        except:
            print(f"Failed to move {filepath}")   
            
            
if __name__=="__main__":
    print(f"Watching folder: {WATCH_FOLDER}")
    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler,path=WATCH_FOLDER,recursive=False)
    observer.start()   
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        
    observer.join()              