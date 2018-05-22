from ctypes import *

from multiprocessing.pool import ThreadPool
import time

class hmp2020:

#конструктор
    def __init__(self,lib,rm_session):
        self.session = c_int32()
        self.rm_session = rm_session
        self.visa64 = lib
        self.viStatus = c_int32()

        self.copy_session  = c_int32()


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
        self.Vistatus = self.visa64.viSetAttribute(self.session,1073676314,0)
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)
        time.sleep(1)
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

    #Функция запроса на установку данных на устройство
    def reedDevice(self):
        start = time.time()
        size_buf = c_ulong()
        buf = create_unicode_buffer(128)
        self.viStatus = self.visa64.viRead(self.session,buf,len(buf),byref(size_buf))
        print(self.viStatus,buf,size_buf)
        print ("reedDevice time: %s" % (time.time()-start))
        return str(buf,'cp1251')



    def viOpen(self,name):
        viStatus = self.visa64.viOpen(self.rm_session,name.encode('utf8'),None,None,byref(self.session))
        print(self.rm_session,viStatus,self.session)


#Функция на подключение устройства
    def connect(self,name):
        #ViStatus = self.visa64.viOpenDefaultRM(byref(self.rm_session))
        self.name = name;
        n = name.split('::')
        print(n[-1])
        #if n[-1] == 'SOCKET':
             #name += '::GEN'

        print(name.encode('utf-8'))

        self.async_func(self.viOpen,[name])

        query=b'*IDN?\n'

        buf = self.queryDevice(query);
        print("buf = " + buf)

        # self.printDevice(b'INST OUT1\n')
        # self.printDevice(b'OUTP:SEL 1\n')
        # self.printDevice(b'INST OUT2\n')
        # self.printDevice(b'OUTP:SEL 1\n')
        self.printDevice(b'OUTPut:GENeral 1\n')
        #
        #

        #
        # query=b'*RST\r\n' #SYSTem:ERRor? *IDN?
        query=b'OUTPut?\r\n'
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
        # self.printDevice(b'INST OUT1\n')
        # self.printDevice(b'OUTP:SEL 0\n')
        # self.printDevice(b'INST OUT2\n')
        # self.printDevice(b'OUTP:SEL 0\n')
        self.printDevice(b'OUTP:GEN 0\n')

        self.visa64.viClose(self.session);
        #self.visa64.viClose(self.rm_session);
