from ..adb import ADB
from ..tools import sleep


class Project:

    def __init__(self, deviceSN):
        self.adbIns = ADB(deviceSN)

    def tapFreeButton(self):
        if 'MI 4' in self.adbIns.device.Model:
            self.adbIns.tap(540, 1706)

    def openApp(self, activity):
        self.adbIns.start(activity)

    def clickByRID(self, resourceID, sleepTime=9):
        self.adbIns.uIA.clickByRID(resourceID)
        sleep(sleepTime)

    def freeMemory(self):
        self.adbIns.pressHomeKey()
        self.adbIns.pressHomeKey()
        self.adbIns.pressMenuKey()
        self.tapFreeButton()

    def mainloop(self):
        pass
