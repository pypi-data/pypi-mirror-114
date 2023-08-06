import xml
from random import randint
from .project import Project
from ..tools import sleep
from datetime import datetime
from time import time
from ..mysql import RetrieveKSJSB, UpdateKSJSB


class ResourceID:
    left_btn = 'com.kuaishou.nebula:id/left_btn'  # 主界面左上角菜单项
    red_packet_anim = 'com.kuaishou.nebula:id/red_packet_anim'  # 主界面右上方红包图标
    cycle_progress = 'com.kuaishou.nebula:id/cycle_progress'  # 金币进度
    gold_egg_anim = 'com.kuaishou.nebula:id/gold_egg_anim'  # 金蛋
    iv_close_common_dialog = 'com.kuaishou.nebula:id/iv_close_common_dialog'  # 主界面右上方关闭奥运夺冠瞬间界面
    animated_image = 'com.kuaishou.nebula:id/animated_image'  # 主界面左上方关闭奥运福娃按钮
    positive = 'com.kuaishou.nebula:id/positive'  # 主界面中间青少年模式，我知道了
    description = 'com.kuaishou.nebula:id/description'  # 网络连接失败，请稍后重试
    tab_text = 'com.kuaishou.nebula:id/tab_text'  # 详细信息/评论
    live_exit_button = 'com.kuaishou.nebula:id/live_exit_button'  # 直接退出（直播）
    exit_btn = 'com.kuaishou.nebula:id/exit_btn'  # 退出（直播）


class Activity:
    HomeActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity'  # 主界面
    MiniAppActivity0 = 'com.kuaishou.nebula/com.mini.app.activity.MiniAppActivity0'  # 小程序
    PhotoDetailActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.detail.PhotoDetailActivity'  # 直播
    TopicDetailActivity = 'com.kuaishou.nebula/com.yxcorp.plugin.tag.topic.TopicDetailActivity'  # 每日书单


class KSJSB(Project):
    instances = []
    startTime = datetime.now()

    def __init__(self, deviceSN):
        super(KSJSB, self).__init__(deviceSN)
        self.sleepTime = 0
        self.lastTime = time()
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

    def getGoldCoins(self):
        pass

    def getCashCoupons(self):
        pass

    def randomSwipe(self):
        if self.sleepTime > 0:
            return
        x1 = randint(520, 550)
        y1 = randint(1530, 1560)
        x2 = randint(520, 550)
        y2 = randint(360, 390)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.sleepTime += randint(3, 15)

    def openApp(self):
        super(KSJSB, self).openApp(Activity.HomeActivity)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def shouldReopen(self):
        pass

    def pressBackKey(self):
        currentFocus = self.adbIns.getCurrentFocus()
        if Activity.MiniAppActivity0 in currentFocus:
            self.adbIns.pressBackKey()
        elif Activity.PhotoDetailActivity in currentFocus:
            self.adbIns.pressBackKey()
            self.uIAIns.click(ResourceID.live_exit_button)
            self.uIAIns.click(ResourceID.exit_btn)
        elif Activity.TopicDetailActivity in currentFocus:
            self.adbIns.pressBackKey()
        elif self.uIAIns.getDict(ResourceID.tab_text):
            self.adbIns.pressBackKey()

    def watchVideo(self):
        self.reopenAppPerHour()
        try:
            self.pressBackKey()
        except (FileNotFoundError, xml.parsers.expat.ExpatError) as e:
            print(e)
        self.sleepTime = self.sleepTime + self.lastTime - time()
        self.lastTime = time()
        self.randomSwipe()

    @classmethod
    def mainloop(cls, devicesSN):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            for i in cls.instances:
                i.watchVideo()
            print('已运行：', datetime.now() - cls.startTime, sep='')
            sleep(1)
