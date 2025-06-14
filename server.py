import socket
from _thread import *
import sys

password = "banana"

def get_local_ip():

    try:
         
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        return local_ip
    
    except Exception as e:
        return "Error: " + e


server = get_local_ip()
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as error_m:
        str(error_m)

s.listen(30)
print("Waiting for a connection, Server Started")

def threaded_client(conn, player):

    conn.send("Game Stuff")
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()

            reply = data

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved:", data)
                print("Sending:", reply)

            conn.sendall(str.encode(reply))
            
        except:
            break

    print("Lost connection")
    conn.close()
            



current_player = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
