import collections
from ..mysql import RetrieveBaseInfo
from os import system, remove
from ..tools import createDir, prettyXML, sleep, findAllNumsWithRe, average
from os.path import exists
import xmltodict


class Node:
    def __init__(self, resourceID, text):
        self.resourceID = resourceID
        self.text = text


class UIAutomator:
    def __init__(self, deviceSN):
        self.device = RetrieveBaseInfo(deviceSN)
        self.cmd = 'adb -s %s ' % self.device.IP
        self.node = Node('', '')

    def getScreen(self):
        system(self.cmd + 'shell rm /sdcard/screencap.png')
        system(self.cmd + 'shell screencap -p /sdcard/screencap.png')
        system(self.cmd + 'pull /sdcard/screencap.png CurrentUIHierarchy/%s.png' % self.device.SN)

    def tap(self, cP, interval=1):
        x, y = cP
        print('正在让%s点击(%d,%d)' % (self.device.SN, x, y))
        system(self.cmd + 'shell input tap %d %d' % (x, y))
        sleep(interval)

    def click(self, resourceID, text=''):
        cP = self.getCP(resourceID, text)
        if not cP:
            return False
        print(cP)
        self.tap(cP)
        return True

    def getCP(self, resourceID, text=''):
        bounds = self.getBounds(resourceID, text)
        if not bounds:
            return False
        x1, y1, x2, y2 = findAllNumsWithRe(bounds)
        x = average(x1, x2)
        y = average(y1, y2)
        return x, y

    def getBounds(self, resourceID, text=''):
        dic = self.getDict(resourceID, text)
        if dic:
            return dic['@bounds']
        return False

    def getDict(self, resourceID, text=''):
        self.node = Node(resourceID, text)
        return self.depthFirstSearch(xmltodict.parse(self.xml))

    def isTargetNode(self, dic):
        if type(dic) in (str, list):
            return False
        if '@resource-id' not in dic.keys():
            return False
        if dic['@resource-id'] == self.node.resourceID:
            if self.node.text:
                if dic['@text'] == self.node.text:
                    return True
                return False
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
