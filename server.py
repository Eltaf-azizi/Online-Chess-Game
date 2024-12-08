import socket
from _thread import *
from board import Board

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = open("ip.txt", "r")
port = 5555

server_ip = socket.gethostbyname(server)

try: 
    s.bind((server, port))

except socket.error as e:
    print(str(e))


s.listen(2)
print("waiting for a connection")

bo = Board(8, 8)

currentId = "w"

def threaded_client(conn):

    global currentId, pos
    conn.send(bo, str.encode(currentId))
    currentId = "b"
    reply = ''

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                

                if reply.count("w") == 1:
                    nid = "b"
                else:
                    nid = "w"

                if id == 0: nid = 1
                if id == 1: nid = 0

                print("Sending: " + reply)


            conn.sendall(str.encode(reply))

        except:
            break

    print("Connection Closed")
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, ))
