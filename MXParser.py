# Create Folder layout

import webbrowser
import zipfile
import os
from typing import Dict
import time

try:
    if not os.path.exists("C:\\MXScout\\"):
        os.makedirs("C:\\MXScout\\")
except Exception as e:
    print(e)

try:
    if not os.path.exists("C:\\MXScout\\SR\\"):
        os.makedirs("C:\\MXScout\\SR\\")
except Exception as e:
    print(e)

try:
    if not os.path.exists("C:\\MXLogs\\"):
        os.makedirs("C:\\MXLogs\\")
except Exception as e:
    print(e)
try:
    if not os.path.exists("C:\\MXLogs\\ZippedFiles\\"):
        os.makedirs("C:\\MXLogs\\ZippedFiles\\")
except Exception as e:
    print(e)
try:
    if not os.path.exists("C:\\MXLogs\\UnzippedFiles\\"):
        os.makedirs("C:\\MXLogs\\UnzippedFiles\\")
except Exception as e:
    print(e)

# Locate and Unzip folders


fileName = input("What is the file name? C:\\MXLogs\\ZippedFiles\\")
SR = str(input("What is the SR or Lightning case number? "))
if not os.path.exists("C:\\MXLogs\\UnzippedFiles\\"+ SR + "\\"):
    os.makedirs("C:\\MXLogs\\UnzippedFiles\\"+ SR + "\\")
if not os.path.exists("C:\\MXScout\\SR\\"+ SR):
    os.makedirs("C:\\MXScout\\SR\\"+ SR)
path_to_zip_file = "C:\\MXLogs\\ZippedFiles\\" + str(fileName)
zip_collection = zipfile.ZipFile(path_to_zip_file, 'r')
zip_collection.extractall("C:\\MXLogs\\UnzippedFiles\\"+ SR + "\\")
zip_collection.close()
extract2 = "C:\\MXLogs\\UnzippedFiles\\" + SR + "\\dumplogs\\ec\\"
for i in os.listdir(extract2):
    if os.path.isfile(os.path.join(extract2,i)) and 'eclogs_active' in i:
        j=zipfile.ZipFile(extract2+i, 'r')
        j.extractall("C:\\MXLogs\\UnzippedFiles\\" + SR + "\\dumplogs\\ec\\")
        j.close()


# Chassis Config Seeker

def ChassisTagSeeker():
    print('Executing ChassisTagSeeker()')
    try:
        file = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\sysinfo.txt', 'r')
        file2 = file.readlines()
        file.close()
        tag = str("")
        for i in file2:
            if 'Service tag#' in i:
                tag = i
                tag = tag.split('#')
                tag = tag[1]
                tag = tag.strip()
                break
            else:
                pass
        return tag
    except Exception as e:
        print(e)
        print("ChassisTagSeeker() failed.")
        return "ChassisTagSeeker() failed."


tag = ChassisTagSeeker()


def Uptimer():
    print('Executing Uptimer()')
    try:
        uptime = str()
        file = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\msm\\active\\system\\commands\\uptime.log', 'r')
        file2 = file.readlines()
        file.close()
        uptime = str('')
        for i in file2:
            uptime = i
            uptime = uptime.split(',')
            uptime = uptime[0]
            uptime = uptime.split('up')[1]
            uptime = "Up for " + str(uptime)

        return uptime
    except Exception as e:
        print(e)
        print('Uptimer() failed.')
        return ('Uptimer() failed.')


uptime = Uptimer()


def MMFWSeeker():
    print('Executing MMFWSeeker()')
    try:
        mm = str()
        file = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\buildlog.txt')
        file = file.readlines()
        for i in file:
            if 'RAC_VERSION_STRING' in i:
                mm = i
        mm = mm.split('=')
        mm = mm[1]
        mm = mm.strip()
        return mm
    except Exception as e:
        print(e)
        return 'MMFWSeeker() failed.'


mm = MMFWSeeker()


def PSUConfig():
    print('Executing PSUConfig()')
    try:
        psconfig = list()
        file = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\powertest.txt')
        file = file.readlines()
        start = file.index('PowerdInfo:\n')
        stop = file.index('Power Attribute:\n')
        ps = file[start:stop - 1]
        ps1 = str()

        return ps

    except Exception as e:
        print(e)
        return "PSUConfig() has failed."


ps = PSUConfig()

powerStr = ''.join(str(x + '<br>') for x in ps)
powerStr.join('<br><br>')

psuDefaultDict = {
    'mfgTime': 'default',
    'manufacturer': 'default',
    'prodName': 'default',
    'serialNum': 'default',
    'partNum': 'default'
}

def PS0Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS0Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu000.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x=x[10:-1]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:-1]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:-1]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:-1]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:-1]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict


psu0 = PS0Seeker(psuDefaultDict)



def PS1Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS1Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu001.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x = x[10:-1]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:-1]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:-1]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:-1]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:-1]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict

psu1=PS1Seeker(psuDefaultDict)


def PS2Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS2Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu002.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x = x[10:-1]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:-1]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:-1]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:-1]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:-1]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict

psu2=PS2Seeker(psuDefaultDict)


def PS3Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS3Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu003.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x = x[10:]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict

psu3=PS3Seeker(psuDefaultDict)


def PS4Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS4Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu004.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x = x[10:]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict

psu4=PS4Seeker(psuDefaultDict)


def PS5Seeker(psuDefaultDict: Dict[str,str]):
    print('Executing PS5Seeker()')
    tmpDict = psuDefaultDict.copy()
    try:
        psu = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\log\\FRUdump\\psu005.txt')
        psu = psu.readlines()
        for x in psu:
            if 'mfg time: ' in x:
                x = x[10:]
                tmpDict.update(mfgTime=x)
                break
        for x in psu:
            if 'manufacturer: ' in x:
                x = x[14:]
                tmpDict.update(manufacturer=x)
                break
        for x in psu:
            if 'product name: ' in x:
                x = x[13:]
                tmpDict.update(prodName=x)
                break
        for x in psu:
            if 'serial number: ' in x:
                x = x[14:]
                tmpDict.update(serialNum=x)
                break
        for x in psu:
            x = x[12:]
            if 'part number: ' in x:
                tmpDict.update(partNum=x)
                break
        return tmpDict
    except Exception as e:
        print(e)
        tmpDict = {
            'mfgTime': 'ERROR!!',
            'manufacturer': 'ERROR!!',
            'prodName': 'ERROR!!',
            'serialNum': 'ERROR!!',
            'partNum': 'ERROR!!'
        }
        return tmpDict

psu5=PS5Seeker(psuDefaultDict)

#Compute info seeker


def Compute():
    print('Executing Compute()')
    try:
        comp= list()
        file= open('C:\\MXLogs\\UnzippedFiles\\'+ SR+ '\\dumplogs\\ec\\system\\jpmtest.txt')
        file=file.readlines()
        start = file.index('jpmtest -C sledd_get_idrac_summary :\n')
        stop = file.index('jpmtest -C sledd_fcc_dump :\n')
        comp = file[start+4:stop-2]
        return comp
    except Exception as e:
        comp = list()
        comp = comp.append('Compute() failed')
        return comp
comp=Compute()

compStr = ''.join(str(x + '<br>') for x in comp)
compStr.join('<br><br>')

'''
sled = file= open('C:\\MXLogs\\UnzippedFiles\\'+ SR+ '\\dumplogs\\ec\\system\\jpmtest.txt')
sled = sled.readlines()
stop = sled.index('**********************************************\n')
sled = sled[5:stop-1]
for x in sled:
    if 'iDRAC: \n' in x:
        
'''

# IOM Seeker replace the below with output from iomdtest in dumplogs/ec/system


iomDict = {
    'protocol': 'default',
    'tag': 'default',
    'HWver': 'default',
    'FWver': 'default',
    'model': 'default'
}


def IOMA1(iomDict: Dict[str,str]):
    print('Executing IOMA1()')
    tmpDict = iomDict.copy()
    try:
        ioma1 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = ioma1.readlines()
        for x in data:
            if "IOM.Slot.A1#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.A1#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.A1#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.A1#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.A1#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMA1() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

ioma1Dict = IOMA1(iomDict)


def IOMA2(iomDict: Dict[str,str]):
    print('Executing IOMA2()')
    tmpDict = iomDict.copy()
    try:
        ioma2 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = ioma2.readlines()
        for x in data:
            if "IOM.Slot.A2#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.A2#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.A2#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.A2#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.A2#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMA2() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

ioma2Dict = IOMA2(iomDict)


def IOMB1(iomDict: Dict[str,str]):
    print('Executing IOMB1()')
    tmpDict = iomDict.copy()
    try:
        iomb1 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = iomb1.readlines()
        for x in data:
            if "IOM.Slot.B1#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.B1#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.B1#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.B1#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.B1#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMB1() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

iomb1Dict = IOMB1(iomDict)


def IOMB2(iomDict: Dict[str,str]):
    print('Executing IOMB2()')
    tmpDict = iomDict.copy()
    try:
        iomb1 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = iomb1.readlines()
        for x in data:
            if "IOM.Slot.B2#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.B2#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.B2#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.B2#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.B2#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMB2() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

iomb2Dict = IOMB2(iomDict)


def IOMC1(iomDict: Dict[str,str]):
    print('Executing IOMC1()')
    tmpDict = iomDict.copy()
    try:
        iomc1 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = iomc1.readlines()
        for x in data:
            if "IOM.Slot.C1#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.C1#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.C1#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.C1#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.C1#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMC1() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

iomc1Dict = IOMC1(iomDict)


def IOMC2(iomDict: Dict[str,str]):
    print('Executing IOMC2()')
    tmpDict = iomDict.copy()
    try:
        iomc2 = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\iomd_test.txt')
        data = iomc2.readlines()
        for x in data:
            if "IOM.Slot.C2#Info.1#ChassisSubType" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(protocol=x)
                break
            else:
                tmpDict.update(protocol='Protocol not found.')
        for x in data:
            if "IOM.Slot.C2#Info.1#HardwareVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(HWver=x)
                break
            else:
                tmpDict.update(HWver='Hardware Version not found.')
        for x in data:
            if "IOM.Slot.C2#Info.1#IOMFWVersion" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(FWver=x)
                break
            else:
                tmpDict.update(FWver='IOM FW version not found.')
        for x in data:
            if "IOM.Slot.C2#Info.1#ServiceTag" in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(tag=x)
                break
            else:
                tmpDict.update(tag="Service Tag not found.")
        for x in data:
            if 'IOM.Slot.C2#Info.1#Model' in x:
                x = x.split('-')
                x = x[1]
                x = x.strip()
                x = x.strip('/n')
                tmpDict.update(model=x)
                break
            else:
                tmpDict.update(model="Model type not found.")
        return tmpDict


    except Exception as e:
        print(e)
        print('IOMC2() Failed')
        tmpDict = {
            'protocol': 'ERROR!!',
            'tag': 'ERROR!!',
            'HWver': 'ERROR!!',
            'FWver': 'ERROR!!',
            'model': 'ERROR!!'
        }

        return tmpDict

iomc2Dict = IOMC2(iomDict)

# Storage seeker

def Stor():
    print('Executing Stor()')
    try:
        storage = open('C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\peripheraltest.txt')
        storage = storage.readlines()
        storCount = storage[3]
        diskCount = storage[4]
        disclaimer = 'C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\peripheraltest.txt'
        storage = storCount + diskCount + disclaimer
        print(storage)
        return storage

    except Exception as e:
        storage = list()
        print(e)
        print('Stor() Failed')
        storage = storage.append('Stor() Failed')
        return storage


stor = Stor()
storDict = {
    'nodes': 'default',
    'disks':'default'
}
storDict.update(nodes=stor[0])
storDict.update(disks=stor[1])


# storStr = "I don't do anything yet!"
# dumplogs/ec/system/peripheraltest.txt

#System Logs
lcl = 'C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\lclwrap_test.txt'
chsmd = 'C:\\MXLogs\\UnzippedFiles\\'+ SR + '\\dumplogs\\ec\\system\\chassismdtest.txt'
sysinfo = 'C:\\MXLogs\\UnzippedFiles\\'+ SR +'\\dumplogs\\ec\\system\\sysinfo.txt'
ip = 'C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\network\\ip.txt'
ifconfig ='C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\network\\ifconfig.txt'
journalctl = 'C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\logs\\journalctl.txt'
periph = 'C:\\MXLogs\\UnzippedFiles\\' + SR + '\\dumplogs\\ec\\system\\peripheraltest.txt'

# HTML

def htmlConstructor():
    print('Executing htmlConstructor(), final task')
    try:
        html1 = open("C:\\MXScout\\SR\\" + SR + "\\" + tag + "-ScoutParsed.html", "w+")
        html1.close()
    except Exception as e:
        print(e)
    try:
        htmlPage = open("C:\\MXScout\\SR\\" + SR + "\\" + tag + "-ScoutParsed.html", "r+")
        message = """
        <!DOCTYPE html>
<html lang="en">
<head>
  <title>MXScout $TAG</title>
    <style>
        h1{background: #007DB8;
                padding: 15px;
                color: white;}
        footer{background: #007DB8;
                padding: 10px;
                color: white;
                text-align: center;
                position: fixed;
                bottom: 0;
                width:100%;}
        h6{padding-left: 15px;}

    </style>
</head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script type='JavaScript'>

</script>

<body>
    <div>
      <h1>MXScout</h1>
    </div>
    <div><h6>Service Tag: $TAG</h6></div>
    <div><h6>MM Revision: $MM</h6></div>
    <div><h6>Uptime: $UPTIME</h6></div>

<div class="btn-group" role="group" style='width: 100%'>
  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#manuals" style="background-color: #007DB8; width: 50%">Manuals</button>
  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#updates" style="background-color: #007DB8; width: 50%">MX Family Downloads</button>


</div>


<div id="manuals" class="collapse">
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx7000/manuals" style="margin-left: 10px;">MX7000 Manuals</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx5016s/manuals" style="margin-left: 10px;">MX5016s Manuals</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx740c/manuals" style="margin-left: 10px;">MX740c Manuals</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx840c/manuals" style="margin-left: 10px;">MX840c Manuals</a> <br>
    <a href="https://www.force10networks.com/CSPortal20/Software/documentation/OS10_Enterprise_Edition_User_Guide_10_4_3_0.pdf" style="margin-left: 10px;">OS10 Manual</a> <br>

  </div>
  <div id="updates" class="collapse">
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx7000/drivers" target="_blank" style="margin-left: 10px;">MX7000</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx5016s/drivers" target="_blank" style="margin-left: 10px;">MX5016s</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx740c/drivers" target="_blank" style="margin-left: 10px;">MX740c</a> <br>
    <a href="https://www.dell.com/support/home/product-support/product/poweredge-mx840c/drivers" target="_blank" style="margin-left: 10px;">MX840c</a> <br>

  </div>
  <br>

<div class="btn-group" role="group" style='width: 100%'>
  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#psus" style="margin-top: 2px; background-color: #007DB8; width: 20%">PSUs</button>
  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#compute" style="margin-top: 2px; background-color: #007DB8; width: 20%">Compute</button>

  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#storage" style="margin-top: 2px; background-color: #007DB8; width: 20%">Storage</button>

  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#ioms" style="margin-top: 2px; background-color: #007DB8; width: 20%">IOMs</button>

  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#quicklogs" style="margin-top: 2px; background-color: #007DB8; width: 20%">System Logs</button>
</div>

    <div id="psus" class="collapse">
        <table style="width:100%">
          <tr>
            <th>PSU 0</th>
            <th>PSU 1</th>
          </tr>
          <tr>
            <td>PS0 Manufacture Time: $PS0MfgTime</td>
            <td>PS1 Manufacture Time: $PS1MfgTime</td>
          </tr>
          <tr>
            <td>PS0 Manufacturer: $PS0Maker</td>
            <td>PS1 Manufacturer: $PS1Maker</td>
          </tr>
          <tr>
            <td>PS0 Details: $PS0ProdName</td>
            <td>PS1 Details: $PS1ProdName</td>
          </tr>
          <tr>
            <td>PS0 Part Number: $PS0PartNum</td>
            <td>PS1 Part Number: $PS1PartNum</td>
          </tr>
          <tr>
            <td>PS0 Serial Number: $PS0SerNum</td>
            <td>PS1 Serial Number: $PS1SerNum</td>
          </tr>
          <tr>
            <th>PSU 2</th>
            <th>PSU 3</th>
          </tr>
          <tr>
            <td>PS2 Manufacture Time: $PS2MfgTime</td>
            <td>PS3 Manufacture Time: $PS3MfgTime</td>
          </tr>
          <tr>
            <td>PS2 Manufacturer: $PS2Maker</td>
            <td>PS3 Manufacturer: $PS3Maker</td>
          </tr>
          <tr>
            <td>PS2 Details: $PS2ProdName</td>
            <td>PS3 Details: $PS3ProdName</td>
          </tr>
          <tr>
            <td>PS2 Part Number: $PS2PartNum</td>
            <td>PS3 Part Number: $PS3PartNum</td>
          </tr>
          <tr>
            <td>PS2 Serial Number: $PS2SerNum</td>
            <td>PS3 Serial Number: $PS3SerNum</td>
          </tr>
          <tr>
            <th>PSU 4</th>
            <th>PSU 5</th>
          </tr>
          <tr>
            <td>PS4 Manufacture Time: $PS4MfgTime</td>
            <td>PS5 Manufacture Time: $PS5MfgTime</td>
          </tr>
          <tr>
            <td>PS4 Manufacturer: $PS4Maker</td>
            <td>PS5 Manufacturer: $PS5Maker</td>
          </tr>
          <tr>
            <td>PS4 Details: $PS4ProdName</td>
            <td>PS5 Details: $PS5ProdName</td>
          </tr>
          <tr>
            <td>PS4 Part Number: $PS4PartNum</td>
            <td>PS5 Part Number: $PS5PartNum</td>
          </tr>
          <tr>
            <td>PS4 Serial Number: $PS4SerNum</td>
            <td>PS5 Serial Number: $PS5SerNum</td>
          </tr>
          </tr> </table>
          <br><br>
          <h4>Power Config: </h4>
          <p>$PSUS</p>
    </div>

    <div id="compute" class="collapse">
        <p>$COMPUTE</p>
    </div>

    <div id="storage" class="collapse">
        <p>This section is under developed and displayed at this time.</p>
        <p>Please review the Peripheral Test file under System Logs.</p>

    </div>

    <div id="ioms" class="collapse">
        <table style="width:100%">
          <tr>
            <th>IOM A1</th>
            <th>IOM A2</th>
          </tr>
          <tr>
              <td>Service Tag: $A1TAG</td>
              <td>Service Tag: $A2TAG</td>
          </tr>
          <tr>
              <td>Firmware version: $A1FW</td>
              <td>Firmware version: $A2FW</td>
          </tr>
          <tr>
              <td>Hardware revision: $A1HW</td>
              <td>Hardware revision: $A2HW</td>
          </tr>
          <tr>
              <td>Connection: $A1PROTO</td>
              <td>Connection: $A2PROTO</td>
          </tr>
          <tr>
              <td>Model: $A1MODEL</td>
              <td>Model: $A2MODEL</td>
          </tr> 
          <tr>
            <th>IOM B1</th>
            <th>IOM B2</th>
          </tr>
          <tr>
              <td>Service Tag: $B1TAG</td>
              <td>Service Tag: $B2TAG</td>
          </tr>
          <tr>
              <td>Firmware version: $B1FW</td>
              <td>Firmware version: $B2FW</td>
          </tr>
          <tr>
              <td>Hardware revision: $B1HW</td>
              <td>Hardware revision: $B2HW</td>
          </tr>
          <tr>
              <td>Connection: $B1PROTO</td>
              <td>Connection: $B2PROTO</td>
          </tr>
          <tr>
              <td>Model: $B1MODEL</td>
              <td>Model: $B2MODEL</td>
          </tr>
          <tr>
            <th>IOM C1</th>
            <th>IOM C2</th>
          </tr>
          <tr>
              <td>Service Tag: $C1TAG</td>
              <td>Service Tag: $C2TAG</td>
          </tr>
          <tr>
              <td>Firmware version: $C1FW</td>
              <td>Firmware version: $C2FW</td>
          </tr>
          <tr>
              <td>Hardware revision: $C1HW</td>
              <td>Hardware revision: $C2HW</td>
          </tr>
          <tr>
              <td>Connection: $C1PROTO</td>
              <td>Connection: $C2PROTO</td>
          </tr>
          <tr>
              <td>Model: $C1MODEL</td>
              <td>Model: $C2MODEL</td>
          </tr>
           </table>
    </div>

    <div id="quicklogs" class="collapse">
        <p><a href="$lclwrap" target="_blank" style="margin-left: 10px;">LCLWrap Test</a> <br>
        <a href="$chassismd" target="_blank" style="margin-left: 10px;">ChassisMD Test</a> <br>
        <a href="$journalctl" target="_blank" style="margin-left: 10px;">Journalctl</a> <br>
        <a href="$sysinfo" target="_blank" style="margin-left: 10px;">Sysinfo</a> <br>
        <a href="$ip" target="_blank" style="margin-left: 10px;">IP Output</a> <br>
        <a href="$ifconfig" target="_blank" style="margin-left: 10px;">Ifconfig Output</a> <br>
        <a href="$periph" target="_blank" style="margin-left: 10px;">Peripheral Test Output</a> <br>
        <a href="$IOMD" target="_blank" style="margin-left: 10px;">Iomd Test Output</a> <br></p>
    </div>

<div>
    <footer id="footer"><a href="mailto:Dylan_Jackson@Dell.com?subject=MXScout Assistance" style="color:white">Application Support</a></footer>
</div>
</html>"""

        if '$TAG' in message:
            message = message.replace('$TAG', tag)
        if '$MM' in message:
            message = message.replace('$MM', mm)
        if '$UPTIME' in message:
            message = message.replace('$UPTIME', uptime)
        if '$PSUS' in message:
            message = message.replace('$PSUS', powerStr)
        if '$PS0MfgTime' in message:
            message = message.replace('$PS0MfgTime', psu0['mfgTime'])
        if '$PS0Maker' in message:
            message = message.replace('$PS0Maker', psu0['manufacturer'])
        if '$PS0ProdName' in message:
            message = message.replace('$PS0ProdName', psu0['prodName'])
        if '$PS0PartNum' in message:
            message = message.replace('$PS0PartNum', psu0['partNum'])
        if '$PS0SerNum' in message:
            message = message.replace('$PS0SerNum', psu0['serialNum'])
        if '$PS1MfgTime' in message:
            message = message.replace('$PS1MfgTime', psu1['mfgTime'])
        if '$PS1Maker' in message:
            message = message.replace('$PS1Maker', psu1['manufacturer'])
        if '$PS1ProdName' in message:
            message = message.replace('$PS1ProdName', psu1['prodName'])
        if '$PS1PartNum' in message:
            message = message.replace('$PS1PartNum', psu1['partNum'])
        if '$PS1SerNum' in message:
            message = message.replace('$PS1SerNum', psu1['serialNum'])
        if '$PS2MfgTime' in message:
            message = message.replace('$PS2MfgTime', psu2['mfgTime'])
        if '$PS2Maker' in message:
            message = message.replace('$PS2Maker', psu2['manufacturer'])
        if '$PS2ProdName' in message:
            message = message.replace('$PS2ProdName', psu2['prodName'])
        if '$PS2PartNum' in message:
            message = message.replace('$PS2PartNum', psu2['partNum'])
        if '$PS2SerNum' in message:
            message = message.replace('$PS2SerNum', psu2['serialNum'])
        if '$PS3MfgTime' in message:
            message = message.replace('$PS3MfgTime', psu3['mfgTime'])
        if '$PS3Maker' in message:
            message = message.replace('$PS3Maker', psu3['manufacturer'])
        if '$PS3ProdName' in message:
            message = message.replace('$PS3ProdName', psu3['prodName'])
        if '$PS3PartNum' in message:
            message = message.replace('$PS3PartNum', psu3['partNum'])
        if '$PS3SerNum' in message:
            message = message.replace('$PS3SerNum', psu3['serialNum'])
        if '$PS4MfgTime' in message:
            message = message.replace('$PS4MfgTime', psu4['mfgTime'])
        if '$PS4Maker' in message:
            message = message.replace('$PS4Maker', psu4['manufacturer'])
        if '$PS4ProdName' in message:
            message = message.replace('$PS4ProdName', psu4['prodName'])
        if '$PS4PartNum' in message:
            message = message.replace('$PS4PartNum', psu4['partNum'])
        if '$PS4SerNum' in message:
            message = message.replace('$PS4SerNum', psu4['serialNum'])
        if '$PS5MfgTime' in message:
            message = message.replace('$PS5MfgTime', psu5['mfgTime'])
        if '$PS5Maker' in message:
            message = message.replace('$PS5Maker', psu5['manufacturer'])
        if '$PS5ProdName' in message:
            message = message.replace('$PS5ProdName', psu5['prodName'])
        if '$PS5PartNum' in message:
            message = message.replace('$PS5PartNum', psu5['partNum'])
        if '$PS5SerNum' in message:
            message = message.replace('$PS5SerNum', psu5['serialNum'])
        if '$COMP' in message:
            message = message.replace('$COMPUTE', compStr)
        if '$DISKS' in message:
            message = message.replace('$DISKS', storDict['disks'])
        if '$NODES' in message:
            message = message.replace('$NODES', storDict['nodes'])
        if '$DISCLAIMER' in message:
            message = message.replace('$DISCLAIMER', stor[2])
        if '$lclwrap' in message:
            message = message.replace('$lclwrap', lcl)
        if '$chassismd' in message:
            message = message.replace('$chassismd', chsmd)
        if '$sysinfo' in message:
            message = message.replace('$sysinfo', sysinfo)
        if '$ip' in message:
            message = message.replace('$ip', ip)
        if '$ifconfig' in message:
            message = message.replace('$ifconfig', ifconfig)
        if '$journalctl' in message:
            message = message.replace('$journalctl', journalctl)
        if '$periph' in message:
            message = message.replace('$periph', periph)
        if '$IOMD' in message:
            message = message.replace('$IOMD', periph)
        if '$A1TAG' in message:
            message = message.replace('$A1TAG', ioma1Dict['tag'])
        if '$A1FW' in message:
            message = message.replace('$A1FW', ioma1Dict['FWver'])
        if '$A1HW' in message:
            message = message.replace('$A1HW', ioma1Dict['HWver'])
        if '$A1PROTO' in message:
            message = message.replace('$A1PROTO', ioma1Dict['protocol'])
        if '$A1MODEL' in message:
            message = message.replace('$A1MODEL', ioma1Dict['model'])
        if '$A2TAG' in message:
            message = message.replace('$A2TAG', ioma2Dict['tag'])
        if '$A2FW' in message:
            message = message.replace('$A2FW', ioma2Dict['FWver'])
        if '$A2HW' in message:
            message = message.replace('$A2HW', ioma2Dict['HWver'])
        if '$A2PROTO' in message:
            message = message.replace('$A2PROTO', ioma2Dict['protocol'])
        if '$A2MODEL' in message:
            message = message.replace('$A2MODEL', ioma2Dict['model'])
        if '$B1TAG' in message:
            message = message.replace('$B1TAG', iomb1Dict['tag'])
        if '$B1FW' in message:
            message = message.replace('$B1FW', iomb1Dict['FWver'])
        if '$B1HW' in message:
            message = message.replace('$B1HW', iomb1Dict['HWver'])
        if '$B1PROTO' in message:
            message = message.replace('$B1PROTO', iomb1Dict['protocol'])
        if '$B1MODEL' in message:
            message = message.replace('$B1MODEL', iomb1Dict['model'])
        if '$B2TAG' in message:
            message = message.replace('$B2TAG', iomb2Dict['tag'])
        if '$B2FW' in message:
            message = message.replace('$B2FW', iomb2Dict['FWver'])
        if '$B2HW' in message:
            message = message.replace('$B2HW', iomb2Dict['HWver'])
        if '$B2PROTO' in message:
            message = message.replace('$B2PROTO', iomb2Dict['protocol'])
        if '$B2MODEL' in message:
            message = message.replace('$B2MODEL', iomb2Dict['model'])
        if '$C1TAG' in message:
            message = message.replace('$C1TAG', iomc1Dict['tag'])
        if '$C1FW' in message:
            message = message.replace('$C1FW', iomc1Dict['FWver'])
        if '$C1HW' in message:
            message = message.replace('$C1HW', iomc1Dict['HWver'])
        if '$C1PROTO' in message:
            message = message.replace('$C1PROTO', iomc1Dict['protocol'])
        if '$C1MODEL' in message:
            message = message.replace('$C1MODEL', iomc1Dict['model'])
        if '$C2TAG' in message:
            message = message.replace('$C2TAG', iomc2Dict['tag'])
        if '$C2FW' in message:
            message = message.replace('$C2FW', iomc2Dict['FWver'])
        if '$C2HW' in message:
            message = message.replace('$C2HW', iomc2Dict['HWver'])
        if '$C2PROTO' in message:
            message = message.replace('$C2PROTO', iomc2Dict['protocol'])
        if '$C2MODEL' in message:
            message = message.replace('$C2MODEL', iomc2Dict['model'])

        htmlPage.write(message)
        htmlPage.close()

    except Exception as e:
        print(e)


htmlConstructor()

print('Parsing complete. Please open the HTML output file in Chrome. The file can be found at: C:\\MXScout\\' +SR+'\\' + tag+'-ScoutParsed.html')
print('This window will self-destruct in 10 seconds.')
time.sleep(10)
#webbrowser.open("file:///C:\\MXScout\\" + SR + "\\" + tag + "-ScoutParsed.html")