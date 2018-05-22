import socket


from multiprocessing.pool import ThreadPool
import time

class udp:

#конструктор
    def __init__(self,):
        self.UDP_IP  = None
        self.UDP_PORT = None
        self.MESSAGE = None
        self.sockserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.datagram = None;
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        print ('Hello from %s' % self.name)

    def async_func(self, name, list):
        pool = ThreadPool(4)
        async_result = pool.apply_async(name,list)
        #pool.close()
        #pool.join()
        result = self.datagram
        return  result

    def startServer(self,ip,port):
        self.sockserver.bind(('', port))
        #self.sockserver.listen(1)
        list = 1
        self.async_func(self.listen,list)


    def listen(self,list):
        self.datagram, addr = self.sock.accept()
        print ('connected:', addr)
        while True:
            data = self.datagram.recv(1024)
            if not data:
                break
            self.datagram.send(data.upper())

    def connect(self,ip,port):
        self.UDP_IP = ip;
        self.UDP_PORT = port
        self.sock.connect((ip, port))




    def write(self,message):
        print("UDP target IP:", self.UDP_IP)
        print("UDP target port:", self.UDP_PORT)
        print("message:", message)
        self.sock.sendto(message.encode('utf8'), (self.UDP_IP, self.UDP_PORT))
        data = self.sock.recv(1024)
        print("Данные от сервера : ", data)
