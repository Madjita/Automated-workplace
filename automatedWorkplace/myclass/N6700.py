from ctypes import *

from multiprocessing.pool import ThreadPool
import time

class n6700:

    #конструктор
    def __init__(self,lib,rm_session):
        self.name = u'' # устанавливаем имя
        self.session = c_uint32()
        self.rm_session = rm_session
        self.visa64 = lib
        self.viStatus = c_uint32()

#Асинхронная функция добавляет выполнение функции в новый поток
    def async_func(self, name, list):
        pool = ThreadPool(4)
        async_result = pool.apply_async(name,list)
        #pool.close()
        #pool.join()
        result = async_result.get()
        return  result


    def viOpen(self,name):
        viStatus = self.visa64.viOpen(self.rm_session,name.encode('utf8'),1,5000,byref(self.session))


#Функция запроса на получение данных от устройства
    def queryDevice(self,query):
        size = c_uint32()
        buf = create_unicode_buffer(2058)

        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)

        self.viStatus = self.visa64.viRead(self.session,buf,len(buf),byref(size))

        print(self.viStatus,str(buf,'cp1251'),size)
        return str(buf.value.encode('utf16'),'cp1251')[2:-1]

#Функция запроса на получение напряжения питания от источника
    def getSetVolt(self, canal):
        vector = []
        if canal == "ALL" or canal == "all":
            vector.append(self.queryDevice(b'VOLTage:LEVel? (@1)\t\n'))
            vector.append(self.queryDevice(b'VOLTage:LEVel? (@2)\t\n'))
            vector.append(self.queryDevice(b'VOLTage:LEVel? (@3)\t\n'))
            vector.append(self.queryDevice(b'VOLTage:LEVel? (@4)\t\n'))
            print(vector)
            return vector
        else:
            if int(canal) == 1:
                vector.append(self.queryDevice(b'VOLTage:LEVel? (@1)\t\n'))
                vector.append(None)
                vector.append(None)
                vector.append(None)
            if int(canal) == 2:
                vector.append(None)
                vector.append(self.queryDevice(b'VOLTage:LEVel? (@2)\t\n'))
                vector.append(None)
                vector.append(None)
            if int(canal) == 3:
                vector.append(None)
                vector.append(None)
                vector.append(self.queryDevice(b'VOLTage:LEVel? (@3)\t\n'))
                vector.append(None)
            if int(canal) == 4:
                vector.append(None)
                vector.append(None)
                vector.append(None)
                vector.append(self.queryDevice(b'VOLTage:LEVel? (@4)\t\n'))
        print(vector)
        return vector

# Функция подачи питания
    def printDevice(self,query):
        size = c_uint32()
        self.viStatus = self.visa64.viWrite(self.session,query,len(query),byref(size))
        print(self.viStatus,query,size)


#Функция на подключение устройства
    def connect(self,name):
        ViStatus = self.visa64.viOpenDefaultRM(byref(self.rm_session))
        self.name = name;
    
        self.async_func(self.viOpen,[name])

        #viStatus = self.visa64.viOpen(self.rm_session,name.encode('utf-8'),None,None,byref(self.session))

        query=b'*IDN?\r\n'
        buf = self.queryDevice(query);
        print("buf = " + buf)

        self.printDevice(b'OUTPut:STATe 1,(@4)\r\n');

        self.getSetVolt("ALL")

        return buf

#Функция на отключение устройства
    def disconnect():
        print("Отключили ->",self.session,self.rm_session)
        self.visa64.viClose(self.session);
        self.visa64.viClose(self.rm_session);
