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
global COUNT
global fromfirst
global strDevice
global strDeviceCodes
global iNumber
strDeviceCodes=["","","","","","","","","",""]
strDevice = "tdevice"
fromfirst = 0
COUNT = 0
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
    global COUNT
    global strDeviceCodes
    AdbDevice = getADBDevice()
    strAdbDevice = str(AdbDevice)
    gettmp = strAdbDevice[fromfirst:]
    COUNT = 0;
    while(gettmp.find(strDevice) != -1):
        strDeviceCodes[COUNT] = FindDeviceCode(gettmp)
        fromfirst = fromfirst + iNumber+7
        gettmp = strAdbDevice[fromfirst:]
        COUNT = COUNT + 1
        
        
#device = MonkeyRunner.waitForConnection()
#easy_device = EasyMonkeyDevice(device)
#hierarchyviewer = device.getHierarchyViewer()
getAllDeviceCode()
global strDeviceCodes
for i in range(0,COUNT):
    print(strDeviceCodes[i])







        