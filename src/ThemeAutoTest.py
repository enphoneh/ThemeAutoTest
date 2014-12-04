#!/usr/bin/python  
#encoding:utf-8
#encoding=gbk
'''
Created on 2014年11月24日

@author: huangyinfeng
'''

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from com.android.monkeyrunner.easy import EasyMonkeyDevice
from com.android.monkeyrunner.easy import By
from com.android.chimpchat.hierarchyviewer import HierarchyViewer

import os
#全局变量
global g_DeviceNumber
global fromfirst
global strDevice
global strDeviceCodes
global iNumber
global g_Apk_Number
global g_PacketName
global g_Activity
global keyboard_26_1080P
global keyboard_26_720P
global keyboard_26_480P
global keyboard_26_320P
global keyboard_9_1080P
global keyboard_9_720P
global keyboard_9_480P
global keyboard_9_320P

keyboard_26_1080P = {'qx':56, 'wx':163, 'ex':272,'rx':377,'tx':484,'yx':593,'ux':702,'ix':809,'ox':918,'px':1029,
            'qy':1347,'wy':1347,'ey':1347,'ry':1347,'ty':1347,'yy':1347,'uy':1347,'iy':1347,'oy':1347,'py':1347,
            'ax':108, 'sx':218, 'dx':328,'fx':438,'gx':548,'hx':658,'jx':768,'kx':878,'lx':988,
            'ay':1512,'sy':1512,'dy':1512,'fy':1512,'gy':1512,'hy':1512,'jy':1512,'ky':1512,'ly':1512,
            'zx':217, 'xx':325,'cx':434,'vx':540,'bx':650,'nx':756,'mx':866,
            'zy':1667,'xy':1667,'cy':1667,'vy':1667,'by':1667,'ny':1667,'my':1667,
            '空格x':642,'上档x':88,'T9x':325,
            '空格y':1840,'上档y':1667,'T9y':1840,
            '回车x':978,
            '回车y':1840}

keyboard_9_1080P = {'1x':290,'2x':533,'3x':777,'4x':290,'5x':533,'6x':777,'7x':290,'8x':533,'9x':777,'0x':533,
                    '1y':1350,'2y':1350,'3y':1350,'4y':1510,'5y':1510,'6y':1510,'7y':1680,'8y':1680,'9y':1680,'0y':1845,
                    'T9x':995,'上档x':995,'符号x':85,'逗号x':85,'回车x':995,
                    'T9y':1510,'上档y':1680,'符号y':1845,'逗号y':1320,'回车y':1845} 

keyboard_26_720P = {'qx':35, 'wx':107, 'ex':179,'rx':251,'tx':323,'yx':396,'ux':470,'ix':536,'ox':615,'px':687,
            'qy':895,'wy':895,'ey':895,'ry':895,'ty':895,'yy':895,'uy':895,'iy':895,'oy':895,'py':895,
            'ax':70, 'sx':145, 'dx':215,'fx':290,'gx':365,'hx':435,'jx':510,'kx':580,'lx':655,
            'ay':1006,'sy':1006,'dy':1006,'fy':1006,'gy':1006,'hy':1006,'jy':1006,'ky':1006,'ly':1006,
            'zx':145, 'xx':215,'cx':290,'vx':365,'bx':435,'nx':510,'mx':580,
            'zy':1119,'xy':1119,'cy':1119,'vy':1119,'by':1119,'ny':1119,'my':1119,
            '空格x':435,'上档x':88,'T9x':215,
            '空格y':1218,'上档y':1119,'T9y':1218,
            '回车x':665,
            '回车y':1218}

keyboard_9_720P = {'1x':190,'2x':355,'3x':518,'4x':190,'5x':355,'6x':518,'7x':190,'8x':355,'9x':518,'0x':355,
                    '1y':900,'2y':900,'3y':900,'4y':1005,'5y':1005,'6y':1005,'7y':1120,'8y':1120,'9y':1120,'0y':1227,
                    'T9x':660,'上档x':660,'符号x':230,'逗号x':52,'回车x':660,
                    'T9y':1005,'上档y':1120,'符号y':1227,'逗号y':880,'回车y':1227} 

strDeviceCodes = []
strDevice = "tdevice"
fromfirst = 0
g_DeviceNumber = 0
g_Apk_Number = 0
g_PacketName = []
g_Activity = []

#函数定义
#倒序输出函数
def RightTOLeft(String):
    strRtoL=""
    for i in range(len(String)-1,0,-1):
        strRtoL+=String[i]
    strRtoL+=String[0]
    return strRtoL

#获取设备
def getADBDevice():
    return os.popen('adb devices').readlines()

#获得机器的机器码
def FindDeviceCode(tmp):
    global strDeviceCodes
    global iNumber
    strDeviceCode="";   
    strTmp = str(tmp)
    iNumber = strTmp.find(strDevice)
    for i in range(iNumber-2,0,-1):
        if strTmp[i]!="\'":
            strDeviceCode+=strTmp[i]
        else:
            break;
    return RightTOLeft(strDeviceCode);

def getAllDeviceCode():
    global fromfirst
    global g_DeviceNumber
    global strDeviceCodes
    AdbDevice = getADBDevice()
    strAdbDevice = str(AdbDevice)
    gettmp = strAdbDevice[fromfirst:]
    g_DeviceNumber = 0;
    while(gettmp.find(strDevice) != -1):
        strDeviceCodes.append(FindDeviceCode(gettmp))
        fromfirst = fromfirst + iNumber+7
        gettmp = strAdbDevice[fromfirst:]
        g_DeviceNumber = g_DeviceNumber + 1
        
def getDeviceConnetion(devicecode):
    return  MonkeyRunner.waitForConnection(10,devicecode)
 
def getDeviceWidth(device):
    return device.getProperty('display.width')

def getDeviceHeight(device):
    return device.getProperty('display.height')

# 获取指定路径下所有指定后缀的文件
# dir 指定路径
# ext 指定后缀，链表&不需要带点 或者不指定。例子：['xml', 'java']
def GetFileFromThisRootDir(dir,ext = None):
    global g_Apk_Number
    allfiles = []
    needExtFilter = (ext != None)
    for root,dirs,files in os.walk(dir):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
                g_Apk_Number = g_Apk_Number + 1
            elif not needExtFilter:
                allfiles.append(filepath)
                g_Apk_Number = g_Apk_Number + 1
    return allfiles
 
def StringExplain(String):
    strTemp = ""
    iFirst = String.find("\'")
    for i in range(iFirst+1,len(String)):
        if String[i] == '\'':
            break
        strTemp = strTemp + String[i]
    return strTemp
 #获取apk包的包名及启动类，并存到全局变量中g_PacketName和g_Activity中   
def getPacketInfo(filepath):
    global g_PacketName
    global g_Activity
    strCmd = "aapt dump badging "+filepath
    temp = os.popen(strCmd).readlines()
    g_PacketName.append(StringExplain(temp[0]))
    g_Activity.append(StringExplain(temp[9]))

def getChildView(self, parentId, *childSeq):
    hierarchyViewer = self.device.getHierarchyViewer()
    str_getchildview="hierarchyViewer.findViewById('" + parentId +"')"    
    for index in childSeq:       
        str_getchildview+=('.children[' + str(index) + ']')         
    return str_getchildview

def ScreenShot(device,deviceName,picName):
    path = "./pic/"+deviceName+"_"+picName+".png"
    result = device.takeSnapshot()
    result.writeToFile(path,'png')
 
def touchbyid(hierarchyviewer,strID):
    view = hierarchyviewer.findViewById(strID)
    MonkeyRunner.sleep(5)
    point = hierarchyviewer.getAbsoluteCenterOfView(view)   #getAbsoluteCenterOfView是HierarchyViewer中的public方法  
    return point
    
def ThemeAutoTest(strDeviceCodes,filepath):
    device = getDeviceConnetion(strDeviceCodes)
    easy_device = EasyMonkeyDevice(device)
    MonkeyRunner.sleep(2)
    hierarchyviewer = device.getHierarchyViewer()
    MonkeyRunner.sleep(2)
    for i in range(0,g_Apk_Number):
       # device.installPackage(filepath[i])
        component= g_PacketName[i]+'/'+g_Activity[i]
        MonkeyRunner.sleep(2)
        device.startActivity(component)
        MonkeyRunner.sleep(2)
        point = touchbyid(hierarchyviewer, 'id/apply_view')
        MonkeyRunner.sleep(3)
        device.touch(point.x,point.y,MonkeyDevice.DOWN_AND_UP)
       # easy_device.touch(By.id('id/apply_view'),MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(2)
        device.press('KEYCODE_BACK ','DOWN_AND_UP')
        MonkeyRunner.sleep(2)
        device.startActivity("com.example.com.jb.gokeyboard.test/com.example.com.jb.gokeyboard.test.MainActivity")
        MonkeyRunner.sleep(2)
        device.touch(80,80,MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(2)
        ScreenShot(device,strDeviceCodes+"_theme"+str(i),'1')
        point = touchbyid(hierarchyviewer, 'id/topmenu_logo_btn')
        MonkeyRunner.sleep(3)
        device.touch(point.x,point.y,MonkeyDevice.DOWN_AND_UP)
        #easy_device.touch(By.id('id/topmenu_center_btn'),MonkeyDevice.DOWN_AND_UP)
        ScreenShot(device,strDeviceCodes+"_theme"+str(i),'2')
        #point = touchbyid(hierarchyviewer, 'id/topmenu_center_btn')
       # MonkeyRunner.sleep(3)
        #device.touch(point.x,point.y,MonkeyDevice.DOWN_AND_UP)
       # easy_device.touch(By.id('id/keyboardlayout_26key'),MonkeyDevice.DOWN_AND_UP)
        #ScreenShot(device,strDeviceCodes+"_theme"+str(i),'3')
        MonkeyRunner.sleep(3)


if __name__ == '__main__':
    global g_DeviceNumber   
    global g_Apk_Number
    getAllDeviceCode()
    global strDeviceCodes
    dir = "/home/huangyinfeng/workspace/ThemeAutoTest/src/apk"
    filepath = GetFileFromThisRootDir(dir,'.apk')
    for i in range(0,g_Apk_Number):
        getPacketInfo(filepath[i])     #获取所有包名和启动acitvity，并存在全局变量packName 与activity中       
    for i in range(0,g_DeviceNumber):
        print(strDeviceCodes[i])      
        ThemeAutoTest(strDeviceCodes[i],filepath)



        