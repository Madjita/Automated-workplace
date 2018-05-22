import os
from ctypes import *

from multiprocessing.pool import ThreadPool
import time

class n9000:
    #конструктор
    def __init__(self,rm_session):
        self.name = u'' # устанавливаем имя
        self.session = c_uint32()
        self.rm_session = rm_session
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.visa64 = WinDLL(self.BASE_DIR + "/Visa/MiVISA32.dll")
        self.viStatus = c_uint32()


    #функция
    def display_info(self):
        print("Примет, меня зовту", self.name)

#Функция запроса на получение данных от устройства
    def queryDevice(self,query):
        size = c_ulong()
        buf = create_unicode_buffer(2058)
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)

        self.viStatus = self.visa64.viRead(self.session,buf,len(buf),byref(size))

        print(self.viStatus,str(buf,'cp1251'),size)
        return str(buf.value.encode('utf16'),'cp1251')[2:-1]

#Функция запроса на установку данных на устройство
    def printDevice(self,query):
        start = time.time()
        size = c_ulong()
        buf = create_unicode_buffer(2058)
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)
        print ("queryDevice " + str(query) + " time: %s" % (time.time()-start))
        return size

#Функция на подключение устройства
    def connect(self,name):
        ViStatus = self.visa64.viOpenDefaultRM(byref(self.rm_session))
        self.name = name;
        viStatus = self.visa64.viOpen(self.rm_session,name.encode('utf-8'),None,None,byref(self.session))

        query=b'*IDN?\r\n'
        buf = self.queryDevice(query);
        print("buf = " + buf)
        return buf

#Функция на отключение устройства
    def disconnect():
        print("Отключили ->",self.session,self.rm_session)
        self.visa64.viClose(self.session);
        self.visa64.viClose(self.rm_session);
