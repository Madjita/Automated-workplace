from ctypes import *

from multiprocessing.pool import ThreadPool
import time

class Micran:

#конструктор
    def __init__(self,lib,rm_session):
        self.session = c_uint32()
        self.rm_session = rm_session
        self.visa64 = lib
        self.viStatus = c_uint32()

        self.copy_session  = c_uint32()


    def run(self):
        print ('Hello from %s' % self.name)

    def async_func(self, name, list):
        pool = ThreadPool(4)
        async_result = pool.apply_async(name,list)
        #pool.close()
        #pool.join()
        result = async_result.get()
        return  result

#функция
    def display_info(self):
        print("Примет, меня зовту", self.name)

#Функция запроса на получение данных от устройства
    def queryDevice(self,query):
        start = time.time()
        size = c_ulong()
        size_buf = c_ulong()
        buf = create_unicode_buffer(256)
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)

        self.viStatus = self.visa64.viRead(self.session,buf,len(buf),byref(size_buf))

        print(self.viStatus,buf,size_buf)

        print ("queryDevice " + str(query) + " time: %s" % (time.time()-start))

        return str(buf,'cp1251')

#Функция запроса на установку данных на устройство
    def printDevice(self,query):
        start = time.time()
        size = c_ulong()
        buf = create_unicode_buffer(2058)
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)

        print ("queryDevice " + str(query) + " time: %s" % (time.time()-start))
        return size


    def viOpen(self,name):
        viStatus = self.visa64.viOpen(self.rm_session,name.encode('utf8'),1,5000,byref(self.session))


#Функция на подключение устройства
    def connect(self,name):
        #ViStatus = self.visa64.viOpenDefaultRM(byref(self.rm_session))
        self.name = name;
        n = name.split('::')
        print(n[-1])
        if n[-1] == 'SOCKET':
             name += '::GEN'

        print(name.encode('utf-8'))

        self.async_func(self.viOpen,[name])

        query=b'*IDN?\r\n'
        buf = self.queryDevice(query);
        print("buf = " + buf)


        self.printDevice(b'INITiate:CONTinuous ON\r\t\n')
        self.printDevice(b'OUTPut:STATe ON\r\t\n')
        #
        #

        #
        # query=b'*RST\r\n' #SYSTem:ERRor? *IDN?
        query=b'OUTPut:STATe?\r\t\n'
        buf = self.queryDevice(query);
        print("buf = " + buf)
        #
        # #self.visa64.viClose(self.session)
        #
        # print(self.rm_session,viStatus,self.session)
        #
        # #buf = self.queryDevice(b'OUTPut:STATe? \r\n');
        # #print("buf = " + buf)
        #
        # #self.visa64.viClose(self.session);
        #

        #self.disconnect();

        # list = []
        # list.append(name);
        # buf = self.async_func(self.cn,list)
        return buf


#Функция на отключение устройства
    def disconnect(self):
        print("Отключили ->",self.session,self.rm_session)
        self.printDevice(b'OUTPut:STATe OFF\r\t\n')
        self.visa64.viClose(self.session);
        #self.visa64.viClose(self.rm_session);
