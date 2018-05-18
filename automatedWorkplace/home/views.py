## -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render, get_object_or_404
from .models import TableAutomatedWorkstation, TableDevice, TableDeviceSerial
from django.http import HttpResponse, JsonResponse

import sys, os , json , codecs
from ctypes import *
from socket import *

#Добавление моего класса
from myclass import N9000, Micran, N6700

# import visa
# visa.log_to_screen()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

visa64 = WinDLL( BASE_DIR + "/Visa/MiVISA32.dll")

rm_session = c_uint32()
session = c_uint32()

ViStatus = visa64.viOpenDefaultRM(byref(rm_session))

# n9000 = N9000.n9000();
#n6700 = N6700.n6700();
# micran = Micran.Micran();
# n = "TCPIP0::10.12.1.100::8888::SOCKET";
#n2= "TCPIP0::10.12.0.149::inst0::INSTR"
#print(n6700.connect(n2))
# print(micran.connect(n))

#myDll = WinDLL( BASE_DIR + "/Visa/DeployDll.dll")



def findDevice():
    expr = b"TCPIP?*"
    instr_list = c_uint32()
    countDevice = c_uint32()
    list  = []
    listDevice = create_unicode_buffer(256)

    ViStatus = visa64.viFindRsrc(rm_session,
                            expr,
                            byref(instr_list),
                            byref(countDevice),
                            listDevice)

    findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
    if len(findStr) > 1:
        findStr[0] = findStr[0][2:-1]
        findStr[2] = findStr[2].split(' ')
        findStr[3] = findStr[0][2:-1].split('::')[1]
    list.append(findStr)

    dontFind = None

    if countDevice.value == 0:
        visa64.viClose(instr_list)
        listDevice = JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : dontFind})
        json_object = json.loads(listDevice.getvalue().decode('utf-8'))
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
            list.append(findStr)

    visa64.viClose(instr_list)
    #return JsonResponse({'desc' : str(desc.value)})
    listDevice =  JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : list})
    json_object = json.loads(listDevice.getvalue().decode('utf-8'))
    print(json_object['listDevice'][0][0])
    return json_object;

def queryDevice(query):
    buf = create_unicode_buffer(20480)
    size = c_ulong()
    viStatus = visa64.viWrite(session,query,len(query),byref(size))
    print(viStatus,query,size)
    viStatus = visa64.viRead(session,buf,len(buf),byref(size))
    print(viStatus,str(buf,'cp1251'),size)
    return str(buf.value.encode('utf16'),'cp1251')[2:-1]

# Create your views here.
def index(request):
    automatedWorkstation = TableAutomatedWorkstation.objects.all()
    json_object = findDevice();

    # name = json_object['listDevice'][0][0];
    # session = c_uint32()
    #
    # viStatus = visa64.viOpen(rm_session,name.encode('utf-8'),None,None,byref(session))
    # print(viStatus,name)


    # instr_list = c_uint32()
    # countDevice = c_uint32()
    # listDevice = create_unicode_buffer(512)
    # rm = visa.ResourceManager()
    # print(rm.list_resources('TCPIP?*'))
    #
    # ud = rm.open_resource(rm.list_resources('TCPIP?*')[0])
    #
    # values = ud.query('*IDN?');
    #
    # print(values)

    #{'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', ['Г7М-20', '10008020
    #'], '10.12.1.100', '']]}

    #{'ViStatus': '0', 'countDevice': '2', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '', ['Г7М-20', '10008020'], '10.12
    #.1.100', ''], ['TCPIP0::10.12.0.149::inst0::INSTR', '', ['N6700B', 'MY54009013'], '10.12.0.149', '\x002.1.100', '']]}


    #listDevice = JsonResponse({'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]})
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
        print("LOLKA connect",  request.GET['name'])
        name = request.GET['name']
        lol = name.split('::')
        print(lol[-1])
        # if lol[-1] == 'SOCKET':
                # name += '::GEN'

        viStatus = visa64.viOpen(rm_session,name.encode('utf-8'),None,None,byref(session))
        #
        # query=b'*IDN?\r\n'
        #
        # buf = queryDevice(query);
        # print("buf = " + buf)

        json_object = findDevice();
        print(json_object)
    return render(request, 'home/rightFindPanel.html', {'listDevice' : json_object })


def disconnect(request):
    if request.method == 'GET':
        print("LOLKA disconnect",  request.GET['name'])
        visa64.viClose(session);
        json_object = findDevice();
        print(json_object)
    return render(request, 'home/rightFindPanel.html', {'listDevice' : json_object })
