import collections
from ..mysql import RetrieveBaseInfo
from os import system, remove
from ..tools import createDir, prettyXML, sleep, findAllNumsWithRe, average
from os.path import exists
import xmltodict


class Node:
    def __init__(self, resourceID):
        self.resourceID = resourceID


class UIAutomator:
    def __init__(self, deviceSN):
        self.device = RetrieveBaseInfo(deviceSN)
        self.cmd = 'adb -s %s ' % self.device.IP
        self.node = Node('')

    def getScreen(self):
        system(self.cmd + 'shell rm /sdcard/screencap.png')
        system(self.cmd + 'shell screencap -p /sdcard/screencap.png')
        system(self.cmd + 'pull /sdcard/screencap.png CurrentUIHierarchy/%s.png' % self.device.SN)

    @classmethod
    def getCP(cls, bounds="[243,270][330,357]"):
        x1, y1, x2, y2 = findAllNumsWithRe(bounds)
        x = average(x1, x2)
        y = average(y1, y2)
        return x, y

    def clickByPoint(self, point):
        x, y = point
        self.tap(x, y)

    def tap(self, x, y, interval=1):
        print('正在让%s点击(%d,%d)' % (self.device.SN, x, y))
        system(self.cmd + 'shell input tap %d %d' % (x, y))
        sleep(interval)

    def click(self, resourceID):
        pass

    def getBounds(self, resourceID):
        pass

    def getDict(self):
        dic = xmltodict.parse(self.xml)
        self.node = Node('com.kuaishou.nebula:id/animated_image')
        self.depthFirstSearch(dic)

    def isTargetNode(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        # print(type(dic), dic['@resource-id'], sep='\n', end='\n\n\n\n')
        if dic['@resource-id'] == self.node.resourceID:
            print(dic['@resource-id'])
            return True
        return False

    def depthFirstSearch(self, dic):
        if type(dic) == collections.OrderedDict:
            if self.isTargetNode(dic):
                print(dic)
            for i in dic.keys():
                if self.isTargetNode(dic[i]):
                    print(i)
                self.depthFirstSearch(dic[i])
        elif type(dic) == list:
            for i in dic:
                self.depthFirstSearch(i)
        elif type(dic) == str:
            pass

    @property
    def xml(self):
        return self.getCurrentUIHierarchy()

    def getCurrentUIHierarchy(self):
        cmd = self.cmd + 'shell rm /sdcard/window_dump.xml'
        system(cmd)
        cmd = self.cmd + 'shell uiautomator dump /sdcard/window_dump.xml'
        system(cmd)
        currentUIHierarchyDirName = 'CurrentUIHierarchy'
        createDir(currentUIHierarchyDirName)
        currentUIHierarchyFilePath = '%s/%s.xml' % (currentUIHierarchyDirName, self.device.SN)
        if exists(currentUIHierarchyFilePath):
            remove(currentUIHierarchyFilePath)
        cmd = '%spull /sdcard/window_dump.xml %s' % (self.cmd, currentUIHierarchyFilePath)
        system(cmd)
        return prettyXML(currentUIHierarchyFilePath)
