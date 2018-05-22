import socket

from multiprocessing.pool import ThreadPool
import time

class gts:
    def __init__(self,):
        self.UDP_IP  = None
        self.UDP_PORT = None
        self.MESSAGE = None
        self.datagram = None;
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #Данные
        self.status_izl = None
        self.att = None
        self.freq_prd = None
        self.uhf_prd = None
        self.dopler_prd = None
        self.freq_prm = None
        self.uhf_prm = None
        self.dopler_prm = None
        self.freq_dds = None
        self.ampl_i = None
        self.ampl_q = None
        self.ph_i = None
        self.ph_q = None
        self.offset_i = None
        self.offset_q = None


    def run(self):
        print ('Hello from %s' % self.name)

    def async_func(self, name, list):
        pool = ThreadPool(4)
        async_result = pool.apply_async(name,list)
        #pool.close()
        #pool.join()
        result = self.datagram
        return  result
# Функция соединения с блоком ГТС
    def connect(self,ip,port):
        self.UDP_IP = ip;
        self.UDP_PORT = port
        self.sock.connect((ip, port))


# Функция отправки сообщения в блок ГТС
    def write(self,
        status_izl,
        att,
        freq_prd,
        uhf_prd,
        dopler_prd,
        freq_prm,
        uhf_prm,
        dopler_prm,
        freq_dds,
        ampl_i,
        ampl_q,
        ph_i,
        ph_q,
        offset_i,
        offset_q):

        message = "write " + str(status_izl) + " " + str(att) + " " + str(freq_prd) + " " + str(uhf_prd) + " " + str(dopler_prd) + " " + str(freq_prm) + " "  + str(uhf_prm) + " " + str(dopler_prm) + " "

        message += str(freq_dds) + " " + str(ampl_i*8) + " " + str(ampl_q*8) + " " +str(ph_i) + " " + str(ph_q) + " " + str(offset_i) + " " + str(offset_q) + " end_datafull ";

        print("UDP target IP:", self.UDP_IP)
        print("UDP target port:", self.UDP_PORT)
        print("message:", message)

        self.sock.sendto(message.encode('utf8'), (self.UDP_IP, self.UDP_PORT))
