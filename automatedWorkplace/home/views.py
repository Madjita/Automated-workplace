## -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render, get_object_or_404
from .models import TableAutomatedWorkstation, TableDevice
from django.http import HttpResponse, JsonResponse

import sys, os , json , codecs
from ctypes import *
import socket

#Добавление моего класса
from myclass import N9000 , Micran , N6700, GSG, Osuilograf , HMP2020
from mysoket import udp

from block import block_gts
from workplace import gts_auto

import time

#from multiprocessing.pool import ThreadPool

import visa
visa.log_to_screen()



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

visa64 = WinDLL( BASE_DIR + "/Visa/MiVISA32.dll")

rm_session = c_uint32()
session = c_uint32()

ViStatus = visa64.viOpenDefaultRM(byref(rm_session))

#Мои устройства
micran = Micran.Micran(visa64,rm_session)
n6700 = N6700.n6700(visa64,rm_session)
n9000 = N9000.n9000(rm_session)
osuilograf = Osuilograf.Osuilograf(rm_session)
gsg = GSG.gsg(rm_session)
hmp2020 = HMP2020.hmp2020(visa64,rm_session)
udp = udp.udp()
gts = block_gts.gts()

gts_auto = gts_auto.gts_auto(n9000,gts)
#myDll = WinDLL( BASE_DIR + "/Visa/micranLib.dll")


# def async_func(name):
#     pool = ThreadPool(4)
#     async_result = pool.apply_async(name,())
#     list = []
#     result = async_result.get()
#
#     list.append(async_result)
#     list.append(result)
#     return  list

# def async_close():
#     return 0

def findDevice():
    start = time.time()
    expr = b'TCPIP?*'
    instr_list = c_uint32()
    countDevice = c_uint32()
    list  = []
    listDevice = create_unicode_buffer(256)

    ViStatus = visa64.viFindRsrc(rm_session,
                            expr,
                            byref(instr_list),
                            byref(countDevice),
                            listDevice)

    print(rm_session,ViStatus,instr_list)

    findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
    if len(findStr) > 1:
        findStr[0] = findStr[0][2:-1]
        findStr[2] = findStr[2].split(' ')
        findStr[3] = findStr[0][2:-1].split('::')[1]
        if findStr[3].split('.')[1] == 'rs':
            findStr[3] = socket.gethostbyname('A-'+findStr[2][0]+'-'+findStr[2][1][5:]+'.local');
            findStr[0] = "TCPIP::"+findStr[3]+"::inst0::INSTR"


    #host = socket.gethostbyname('A-'+json_object[0][]+'-20895.local');
    #print (host)

    list.append(findStr)

    dontFind = None

    if countDevice.value == 0:
        visa64.viClose(instr_list)
        listDevice = JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : dontFind})
        json_object = json.loads(listDevice.getvalue().decode('utf-8'))
        print ("Поиск устройств занял time: %s" % (time.time()-start))
        return json_object;
    else:
        for countDevices in range(countDevice.value-1):
            ViStatus = visa64.viFindNext(instr_list,listDevice)
            print(findStr)
            #list.append(str(listDevice.value)[2:-1])
            findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
            findStr[0] = findStr[0][2:-1]
            findStr[2] = findStr[2].split(' ')
            findStr[3] = findStr[0][2:-1].split('::')[1]
            if findStr[3].split('.')[1] == 'rs':
                findStr[3] = socket.gethostbyname('A-'+findStr[2][0]+'-'+findStr[2][1][5:]+'.local');
                findStr[0] = "TCPIP::"+findStr[3]+"::inst0::INSTR"

            list.append(findStr)

    visa64.viClose(instr_list)
    #return JsonResponse({'desc' : str(desc.value)})
    listDevice =  JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : list})
    json_object = json.loads(listDevice.getvalue().decode('utf-8'))

    print ("Поиск устройств занял time: %s" % (time.time()-start))

    print(json_object['listDevice'])
    return json_object;

def queryDevice(query):
    start = time.time()
    buf = create_unicode_buffer(20480)
    size = c_ulong()
    viStatus = visa64.viWrite(session,query,len(query),byref(size))
    print(viStatus,query,size)
    viStatus = visa64.viRead(session,buf,len(buf),byref(size))
    print(viStatus,str(buf,'cp1251'),size)
    print ("queryDevice " + str(query) + " time: %s" % (time.time()-start))
    return str(buf.value.encode('utf16'),'cp1251')[2:-1]

# Create your views here.
def index(request):
    automatedWorkstation = TableAutomatedWorkstation.objects.all()
    json_object = findDevice()

    # freq_prd = (950-950)*100;
    # freq_prm = (950-950)*100;
    # ampl_i = 4095
    # ampl_q = ampl_i;
    #
    # gts.write(1,0,freq_prd,0,0,freq_prm,0,0,0,ampl_i,ampl_q,0,0,0,0);
    #udp.startServer('',9090)

    #udp.connect('10.12.1.100',8888)
    #udp.write('*IDN?\r\t\n')

    #myDll._ZN9MicranLib10DisConnectEv("10.12.1.100");


    #micran.connect('TCPIP0::10.12.1.100::8888::SOCKET')
    #json_object = async_func(name=findDevice)[1]

    #json_object = async_func(name=findDevice)

    #n9000 = N9000.n9000();
    #n6700 = N6700.n6700();



    #n = "TCPIP0::10.12.1.100::8888::SOCKET";
    #n2= "TCPIP0::10.12.0.149::inst0::INSTR"
    #print(n6700.connect(n2))



    # name = json_object['listDevice'][0][0];
    # session = c_uint32()
    #
    # viStatus = visa64.viOpen(rm_session,name.encode('utf-8'),None,None,byref(session))
    # print(viStatus,name)


    # instr_list = c_uint32()
    # countDevice = c_uint32()
    # listDevice = create_unicode_buffer(512)
    #rm = visa.ResourceManager()
    #print(rm.list_resources('TCPIP?*'))
    #
    #print( ("TCPIP::10.12.1.100::8888::SOKET::GEN")) #'TCPIP?*'
    #print(rm.list_resources(query=b'?*'));
    #my_instrument = rm.open_resource('TCPIP0::10.12.1.100::8888::SOKET')
    #ud = rm.open_resource(b'TCPIP::10.12.1.100::8888::SOKET::GEN')    #rm.list_resources('TCPIP?*')[0])
    #
    #values = ud.query('*IDN?');

    #values = ud.write(b'OUTPut:STATe ON\r\n')
    #
    # print(values)

    #{'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', ['Г7М-20', '10008020
    #'], '10.12.1.100', '']]}

    #{'ViStatus': '0', 'countDevice': '2', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '', ['Г7М-20', '10008020'], '10.12
    #.1.100', ''], ['TCPIP0::10.12.0.149::inst0::INSTR', '', ['N6700B', 'MY54009013'], '10.12.0.149', '\x002.1.100', '']]}


    #listDevice = JsonResponse({'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', ['Г7М-20', '10008020'], '10.12.1.100', '']]})
    #json_object = json.loads(listDevice.getvalue().decode('utf-8'))
    #print(str(listDevice.getvalue().decode('utf-8')))
    #return listDevice

    #print(myDll.DeployDll())
    #print(myDll.showMessage())
    #{'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]}

    return render(request, 'home/index.html', {'automatedWorkstation': automatedWorkstation, 'listDevice' : json_object })

def findDeviceHtml(request):
    print("LOLKA findDeviceHtml")
    json_object = findDevice();
    print(json_object)
    return render(request, 'home/rightFindPanel.html', {'listDevice' : json_object })

def connect(request):
    if request.method == 'GET':
        name = request.GET['name']
        type = request.GET['type']
        print("LOLKA connect",  name,type)

        if type == 'Г7М-20':
            micran.connect(name)
        elif type == 'N6700B':
            n6700.connect(name)
        elif type == 'N9030A':
                gts.connect('192.168.1.10',5548)
                n9000.connect(name)
                gts_auto.startWork()

        #hmp2020.connect('TCPIP::10.12.1.9::5025::SOCKET')


        #micran.connect(name)

        # viStatus = visa64.viOpen(rm_session,name.encode('utf8'),None,None,byref(session))
        #
        # #
        # data = b'*IDN?\r\n'
        # #
        # buf = queryDevice(data)
        # print("buf = " + buf)
        # visa64.viClose(session)

        # json_object = async_func(name=findDevice)
        #
        # lol = json_object[0]
        # print(lol)
        # #lol.wait()
        # json_object = json_object[1]
        #
        # l = async_func(name=lol24)[0]


        json_object = findDevice();




        print(json_object)
        return render(request, 'home/rightFindPanel.html', {'listDevice' : json_object })


def disconnect(request):
    if request.method == 'GET':
        name = request.GET['name']
        type = request.GET['type']
        print("LOLKA connect",  name,type)

        if type == 'Г7М-20':
            micran.disconnect()
        elif type == 'N6700B':
            n6700.disconnect()

        #hmp2020.disconnect()

        visa64.viClose(session);
        print(session)
        json_object = findDevice();
        #json_object = async_func(name=findDevice)[1]
        print(json_object)
    return render(request, 'home/rightFindPanel.html', {'listDevice' : json_object })

def lol24():
    c = 0
    while 1:
        if session == 0:
            self.stoped = true
        c +=1
        print (c)
