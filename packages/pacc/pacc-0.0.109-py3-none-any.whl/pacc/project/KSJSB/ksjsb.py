import xml
from random import randint
from datetime import datetime
from time import time
from ...tools import sleep
from ...mysql import RetrieveKSJSB, UpdateKSJSB
from ...Multi import runThread, threadLock
from ..project import Project
from . import resourceID, activity


class KSJSB(Project):
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.restTime = 0
        self.lastTime = time()
        self.dbr = RetrieveKSJSB(deviceSN)

    def updateGoldCoins(self):
        self.reopenApp()
        self.clickByRID(resourceID.red_packet_anim)
        goldCoins = self.getGoldCoins()
        cashCoupons = self.getCashCoupons()
        if not goldCoins == self.dbr.goldCoins:
            UpdateKSJSB(self.adbIns.device.SN).updateGoldCoins(goldCoins)
        if not cashCoupons == self.dbr.cashCoupons:
            UpdateKSJSB(self.adbIns.device.SN).updateCashCoupons(cashCoupons)

    def getGoldCoins(self):
        pass

    def getCashCoupons(self):
        pass

    def randomSwipe(self):
        if self.restTime > 0:
            return
        x1 = randint(520, 550)
        y1 = randint(1530, 1560)
        x2 = randint(520, 550)
        y2 = randint(360, 390)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.restTime += randint(3, 15)

    def openApp(self):
        super(KSJSB, self).openApp(activity.HomeActivity)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def shouldReopen(self):
        pass

    def pressBackKey(self):
        currentFocus = self.adbIns.getCurrentFocus()
        activities = [
            activity.PhotoDetailActivity,
            activity.MiniAppActivity0,
            activity.TopicDetailActivity,
            activity.UserProfileActivity,
            activity.AdYodaActivity
        ]
        for a in activities:
            if a in currentFocus:
                self.adbIns.pressBackKey()
                break
        if self.uIAIns.getDict(resourceID.tab_text):
            self.adbIns.pressBackKey()
        elif self.uIAIns.getDict(resourceID.comment_header_close, xml=self.uIAIns.xml):
            self.adbIns.pressBackKey()
        self.uIAIns.click(resourceID.live_exit_button, xml=self.uIAIns.xml)
        self.uIAIns.click(resourceID.exit_btn, xml=self.uIAIns.xml)
        self.uIAIns.click(resourceID.button2, xml=self.uIAIns.xml)

    def initSleepTime(self):
        print('restTime=%s' % self.restTime)
        if self.restTime <= 0:
            return
        elif self.uIAIns.getDict(resourceID.live_simple_play_swipe_text, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(resourceID.open_long_atlas, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(resourceID.choose_tv, xml=self.uIAIns.xml):
            pass
        else:
            return
        self.restTime = 0

    def watchVideo(self):
        self.reopenAppPerHour()
        try:
            self.pressBackKey()
            self.initSleepTime()
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
        self.restTime = self.restTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()
        self.uIAIns.xml = ''

    @classmethod
    def initIns(cls, deviceSN):
        ins = cls(deviceSN)
        threadLock.acquire()
        cls.instances.append(ins)
        threadLock.release()

    @classmethod
    def mainloop(cls, devicesSN):
        threads = []
        for deviceSN in devicesSN:
            t = runThread(cls.initIns, (deviceSN, ))
            sleep(1)
            threads.append(t)
        for t in threads:
            t.join()
        while True:
            for i in cls.instances:
                i.watchVideo()
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime, sep='')
            sleep(1)
