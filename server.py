import socket
from _thread import *
import sys

server = ""
port = 5555

s = socket.socket(socket.AF_NET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
        str(e)

s.listen(25)
print("Waiting for a connection, Server Started")

def threaded_client(conn):

    reply = ""
    
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            




while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
