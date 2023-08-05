from random import randint
from .project import Project
from ..tools import sleep, EMail, xtd
from datetime import datetime
from ..mysql import RetrieveKSJSB, UpdateKSJSB


class ResourceID:
    left_btn = 'com.kuaishou.nebula:id/left_btn'  # 主界面左上角菜单项
    red_packet_anim = 'com.kuaishou.nebula:id/red_packet_anim'  # 主界面右上方红包图标


class Activity:
    HomeActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity'


class KSJSB(Project):
    rID = ResourceID()
    verificationCode = 'com.kuaishou.nebula/com.yxcorp.gifshow.webview.KwaiYodaWebViewActivity'
    shopping = 'kuaishou.nebula/com.kuaishou.merchant.basic.MerchantYodaWebViewActivity'
    liveStreaming = 'com.kuaishou.nebula/com.yxcorp.gifshow.detail.PhotoDetailActivity'
    userProfileActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.profile.activity.UserProfileActivity'
    recentsActivity = 'com.android.systemui/com.android.systemui.recents.RecentsActivity'
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.sleepTime = 0
        self.dbr = RetrieveKSJSB(deviceSN)

    def updateGoldCoins(self):
        self.reopenApp()
        self.clickByRID(ResourceID.red_packet_anim)
        goldCoins = self.getGoldCoins()
        cashCoupons = self.getCashCoupons()
        if not goldCoins == self.dbr.goldCoins:
            UpdateKSJSB(self.adbIns.device.SN).updateGoldCoins(goldCoins)
        if not cashCoupons == self.dbr.cashCoupons:
            UpdateKSJSB(self.adbIns.device.SN).updateCashCoupons(cashCoupons)

    def getXMLData(self):
        self.adbIns.getCurrentUIHierarchy()
        return xtd('CurrentUIHierarchy/%s.xml' % self.adbIns.device.SN)

    def getGoldCoins(self):
        d = self.getXMLData()
        d = d['hierarchy']['node']['node']['node']['node']['node']['node']['node'][1]
        d = d['node']['node']['node'][1]['node'][0]
        return d['node'][0]['@text']

    def getCashCoupons(self):
        d = self.getXMLData()
        d = d['hierarchy']['node']['node']['node']['node']['node']['node']['node'][1]
        d = d['node']['node']['node'][1]['node'][1]
        return d['node'][0]['@text']

    def randomSwipe(self):
        if self.sleepTime > 0:
            return
        x1 = randint(500, 560)
        y1 = randint(1500, 1590)
        x2 = randint(500, 560)
        y2 = randint(360, 560)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.sleepTime += randint(3, 15)

    def openApp(self):
        super(KSJSB, self).openApp(Activity.HomeActivity)

    def reopenApp(self, reboot=False, sleepTime=6):
        if reboot:
            self.adbIns.reboot()
        self.freeMemory()
        self.openApp()
        sleep(sleepTime)

    def watchVideo(self, st):
        if self.adbIns.rebootPerHour():
            self.reopenApp()
        self.randomSwipe()
        self.sleepTime -= st
        currentFocus = self.adbIns.getCurrentFocus()
        if self.shouldReopen(currentFocus) or self.verificationCode in currentFocus:
            self.reopenApp()
        # elif self.verificationCode in currentFocus:
        #     EMail(self.adbIns.device.SN).sendVerificationCodeAlarm()

    def shouldReopen(self, currentFocus):
        if self.liveStreaming in currentFocus:
            return True
        elif self.userProfileActivity in currentFocus:
            return True
        elif self.shopping in currentFocus:
            return True
        elif self.recentsActivity in currentFocus:
            return True
        return False

    @classmethod
    def mainloop(cls, devicesSN=['301', '302', '303']):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            st = randint(3, 9)
            for i in cls.instances:
                i.watchVideo(st)
            print('已运行：', datetime.now() - cls.startTime, sep='')
            sleep(st)
