import collections
from ..mysql import RetrieveBaseInfo
from os import system, remove
from ..tools import createDir, prettyXML, sleep, findAllNumsWithRe, average
from os.path import exists
import xmltodict
import xml


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

    def clickByPoint(self, point):
        x, y = point
        self.tap(x, y)

    def tap(self, x, y, interval=1):
        print('正在让%s点击(%d,%d)' % (self.device.SN, x, y))
        system(self.cmd + 'shell input tap %d %d' % (x, y))
        sleep(interval)

    def click(self, resourceID):
        cP = self.getCP(resourceID)
        if not cP:
            return False
        self.tap(cP)
        return True

    def getCP(self, resourceID):
        bounds = self.getBounds(resourceID)
        if not bounds:
            return False
        x1, y1, x2, y2 = findAllNumsWithRe(bounds)
        x = average(x1, x2)
        y = average(y1, y2)
        return x, y

    def getBounds(self, resourceID):
        return self.getDict(resourceID)['@bounds']

    def getDict(self, resourceID):
        try:
            dic = xmltodict.parse(self.xml)
        except xml.parsers.expat.ExpatError as e:
            print(e)
            return self.getDict(resourceID)
        self.node = Node(resourceID)
        return self.depthFirstSearch(dic)

    def isTargetNode(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if dic['@resource-id'] == self.node.resourceID:
            return True
        return False

    def depthFirstSearch(self, dic):
        if type(dic) == collections.OrderedDict:
            if self.isTargetNode(dic):
                return dic
            for i in dic.keys():
                if self.isTargetNode(dic[i]):
                    return dic[i]
                res = self.depthFirstSearch(dic[i])
                if res:
                    return res
        elif type(dic) == list:
            for i in dic:
                res = self.depthFirstSearch(i)
                if res:
                    return res

    @property
    def xml(self):
        return self.getCurrentUIHierarchy()

    def getCurrentUIHierarchy(self):
        system(self.cmd + 'shell rm /sdcard/window_dump.xml')
        system(self.cmd + 'shell uiautomator dump /sdcard/window_dump.xml')
        currentUIHierarchyDirName = 'CurrentUIHierarchy'
        createDir(currentUIHierarchyDirName)
        currentUIHierarchyFilePath = '%s/%s.xml' % (currentUIHierarchyDirName, self.device.SN)
        print(currentUIHierarchyFilePath)
        if exists(currentUIHierarchyFilePath):
            remove(currentUIHierarchyFilePath)
        system('%spull /sdcard/window_dump.xml %s' % (self.cmd, currentUIHierarchyFilePath))
        return prettyXML(currentUIHierarchyFilePath)
