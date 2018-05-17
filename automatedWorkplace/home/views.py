## -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render, get_object_or_404
from .models import TableAutomatedWorkstation, TableDevice, TableDeviceSerial
from django.http import HttpResponse, JsonResponse

import sys, os , json , codecs
from ctypes import *
from socket import *

#import visa
#visa.log_to_screen()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

visa64 = WinDLL( BASE_DIR + "/Visa/MiVISA32.dll")

rm_session = c_uint32()
session = c_uint32()
ViStatus = visa64.viOpenDefaultRM(byref(rm_session))


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

    #list.append(str(listDevice.value)[2:-1])


    findStr = str(listDevice.value.encode('utf16'),'cp1251').split('\t')
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
    #rm = visa.ResourceManager()
    #print(rm.list_resources('TCPIP?*'))
    #listDevice = JsonResponse({'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]})
    #print(str(listDevice.getvalue().decode('utf-8')))
    #return listDevice

    #print(myDll.DeployDll())
    #print(myDll.showMessage())
    #{'ViStatus': '0', 'countDevice': '1', 'listDevice': [['TCPIP0::10.12.1.100::8888::SOCKET', '10.12.1.66', 'Г7М-20 10008020', '10.12.1.100', '']]}




    return render(request, 'home/index.html', {'automatedWorkstation': automatedWorkstation, 'listDevice' : json_object })

def connect(request):
    if request.method == 'GET':
        print("LOLKA",  request.GET['name'])
        name = request.GET['name']
        viStatus = visa64.viOpen(rm_session,name.encode('utf-8'),None,None,byref(session))
        print(viStatus,name)
    return HttpResponse(request)

def disconnect(request):
    if request.method == 'GET':
        print("LOLKA disconnect",  request.GET['name'])
        name = request.GET['name']
        print(name)
        visa64.viClose(session);
    return HttpResponse(request)


    #
    # YOUR_OBJECT.objects.filter(name=name).update(view=F('views')+1)
    # return HttpResponseRedirect(request.Get.get('next'))
