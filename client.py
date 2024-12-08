import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "157.230.230.181"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.board, self.id = self.connect()
        self.board = pickle.loads(self.board)


    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()
    


    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        
        except socket.error as e:
            return str(e)
        

n = Network()
n.send("hello")
print(n.id)
