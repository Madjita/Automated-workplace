## -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render, get_object_or_404
from .models import TableAutomatedWorkstation, TableDevice, TableDeviceSerial
from django.http import HttpResponse, JsonResponse

import sys, os , json , codecs
from ctypes import *
from socket import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

visa64 = WinDLL( BASE_DIR + "/Visa/MiVISA32.dll")

myDll = WinDLL( BASE_DIR + "/Visa/DeployDll.dll")



def findDevice():
    rm_session = c_uint32()
    ViStatus = visa64.viOpenDefaultRM(byref(rm_session))

    expr = b"TCPIP?*"
    instr_list = c_uint32()
    countDevice = c_uint32()

    list  = []

    listDevice = create_unicode_buffer(512)

    ViStatus = visa64.viFindRsrc(rm_session,
                            expr,
                            byref(instr_list),
                            byref(countDevice),
                            listDevice)

    #list.append(str(listDevice.value)[2:-1])


    findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
    findStr[0] = findStr[0][2:-1]
    list.append(findStr)



    dontFind = None

    if countDevice.value == 0:
        return JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : dontFind})
    else:
        for countDevices in range(countDevice.value-1):
            ViStatus = visa64.viFindNext(instr_list,listDevice)
            #list.append(str(listDevice.value)[2:-1])
            findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
            findStr[0] = findStr[0][2:-1]
            list.append(findStr)




    #return JsonResponse({'desc' : str(desc.value)})
    return JsonResponse({'ViStatus' : str(ViStatus) ,'countDevice': str(countDevice.value) ,'listDevice' : list})


# Create your views here.
def index(request):
    automatedWorkstation = TableAutomatedWorkstation.objects.all()

    listDevice = findDevice();



    listDevice = JsonResponse({'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]})



    #print(str(listDevice.getvalue().decode('utf-8')))

    #return listDevice

    json_object = json.loads(listDevice.getvalue().decode('utf-8'))



    print(json_object['listDevice'])


    print(myDll.DeployDll())
    print(myDll.showMessage())


    #{'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]}



    return render(request, 'home/index.html', {'automatedWorkstation': automatedWorkstation, 'listDevice' : json_object })
