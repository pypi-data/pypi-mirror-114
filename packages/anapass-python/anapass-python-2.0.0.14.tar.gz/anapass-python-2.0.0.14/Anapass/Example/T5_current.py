from Anapass.TModule import *
import time

t5_dev = TDevice(TDevice.Type.T5)

isConnect = t5_dev.Connect()

if isConnect:
    print('Connection Success')
    t5_power = TPower()
    time.sleep(1)
else:
    print('Check Connections')

cmd = 'ACT\tVLIN1\tVDDI\tVCI\tVDDR\n'

fwrite = open('current test.txt','w')
fwrite.write(cmd)
fwrite.close()
c = input('Press Enter key after IP Write')

itera = 10
for i in range(10):
    ILIN1, IDD1, ICI, IDDR = [], [], [], []
    t5_dev.Next()
    print('ACT' + str(i+2))
    time.sleep(5)
    for j in range(itera):
        isOK = t5_dev.CatchPower(t5_power)
        ILIN1.append(t5_power.Current[0])
        IDD1.append(t5_power.Current[2])
        ICI.append(t5_power.Current[3])
        IDDR.append(t5_power.Current[5])
    vlin1 = str(round(sum(ILIN1)/itera,2)) + '\t'
    vdd1 = str(round(sum(IDD1)/itera,2)) + '\t'
    vci = str(round(sum(ICI)/itera,2)) + '\t'
    vddr = str(round(sum(IDDR)/itera,2)) + '\n'
    cmd = 'ACT'+ str(i+2) +'\t'  + vlin1 + vdd1 + vci + vddr
    fwrite = open('current test.txt', 'a+')
    fwrite.write(cmd)
    fwrite.close()
    
