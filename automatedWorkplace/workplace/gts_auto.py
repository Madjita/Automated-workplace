import socket

from myclass import N9000


from multiprocessing.pool import ThreadPool
import time

class gts_auto:
    def __init__(self,n9000,gts):
        self.gts = gts
        self.n9000 = n9000
        self.listRezulr = []

    def async_func(self, name, list):
        pool = ThreadPool(4)
        async_result = pool.apply_async(name,list)
        #pool.close()
        #pool.join()
        # result = async_result.get()
        # return result



    def proverka_1(self):
        print("=================\n");
        print("Старт 1 проверка\n");
        dResultY = 0;
        dResultX = 0;

        x = []
        y = []

        GnFREQuencyStep = 10 ; #(МГЦ)
        GnFREQuencyStep_kHz = 10; # Кгц

        GnFREQuencyStart = 950;
        GnFREQuencyEnd = 2150;

        end = GnFREQuencyStart;

        freq_prd = GnFREQuencyStart;
        freq_prm = GnFREQuencyStart;

        ampl_i = 4095;
        ampl_q = ampl_i;

        self.n9000.printDevice(b'BWidth:RES 100 kHz\r\n')
        self.n9000.printDevice(b'BWidth:VID 100 kHz\r\n')

        self.n9000.printDevice(b'DISP:WIND:TRAC:Y:RLEV 10 dBm\r\n')

        freq = None;
        NeravnACHX = None;

        good = True;

        while GnFREQuencyEnd >= end:
            freq_prd = (end-950)*100;
            freq_prm = (end-950)*100;
            #Задает полосу просмотра для отображения сигнала на анализаторе....
            self.n9000.printDevice(b'FREQuency:STARt %d MHz\r\n' % (end-GnFREQuencyStep)); #*1000
            self.n9000.printDevice(b'FREQuency:STOP %d MHz\r\n' % (end+GnFREQuencyStep)); #*1000
            self.gts.write(1,0,freq_prd,0,0,freq_prm,0,0,0,ampl_i,ampl_q,0,0,0,0);
            time.sleep(0.15)
            self.n9000.printDevice(b'CALC:MARK:MAX\n')
            dResultY = self.n9000.queryDevice(b'CALC:MARK:Y?\n')
            dResultX = self.n9000.queryDevice(b'CALC:MARK:X?\n')
            self.gts.write(1,0,freq_prd,0,0,freq_prm,0,0,0,ampl_i,ampl_q,0,0,0,0);
            time.sleep(0.15)
            self.n9000.printDevice(b'CALC:MARK:MAX\n')
            dResultY = self.n9000.queryDevice(b'CALC:MARK:Y?\n')
            dResultX = self.n9000.queryDevice(b'CALC:MARK:X?\n')
            print(dResultY,dResultX)
            freq = float(dResultX) / pow(10,6);
            x.append(freq);

            if float(dResultY) >= -60:
                y.append(float(dResultY));
            else:
                y.append(float(dResultY));
                good = False
                print("СРЫВ")

            NeravnACHX = float(max(y)-min(y))
            end+=GnFREQuencyStep;
            print("signal  updateGraph")
        print(x)
        print(y)
        print('Неравномерность = ', NeravnACHX)
        good2 = true
        if float(NeravnACHX) <= 6:
            good2 = True
        else:
            good2 = False

        listGood = []
        listGood.append(good)
        listGood.append(good2)
        return listGood


    def work(self):
        self.listRezulr = []
        p1 = self.proverka_1()
        print(p1)
        self.listRezulr.apend(p1)
        return rezult

    def startWork(self):
        self.async_func(self.work,())
        return 0
