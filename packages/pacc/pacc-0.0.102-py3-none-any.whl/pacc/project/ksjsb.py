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
    live_simple_play_swipe_text = 'com.kuaishou.nebula:id/live_simple_play_swipe_text'  # 点击进入直播间
    open_long_atlas = 'com.kuaishou.nebula:id/open_long_atlas'  # 点击打开长图
    comment_header_close = 'com.kuaishou.nebula:id/comment_header_close'  # 关闭评论
    button2 = 'android:id/button2'  # 等待按钮（应用长时间无反应）
    choose_tv = 'com.kuaishou.nebula:id/choose_tv'  # 请选择你要进行的操作（不感兴趣、关注）


class Activity:
    HomeActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity'  # 主界面
    PhotoDetailActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.detail.PhotoDetailActivity'  # 直播
    MiniAppActivity0 = 'com.kuaishou.nebula/com.mini.app.activity.MiniAppActivity0'  # 小程序
    TopicDetailActivity = 'com.kuaishou.nebula/com.yxcorp.plugin.tag.topic.TopicDetailActivity'  # 每日书单
    UserProfileActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.profile.activity.UserProfileActivity'  # 用户主页
    AdYodaActivity = 'com.kuaishou.nebula/com.yxcorp.gifshow.ad.webview.AdYodaActivity'  # 广告


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
        if self.restTime > 0:
            return
        x1 = randint(520, 550)
        y1 = randint(1530, 1560)
        x2 = randint(520, 550)
        y2 = randint(360, 390)
        self.adbIns.swipe(x1, y1, x2, y2)
        self.restTime += randint(3, 15)

    def openApp(self):
        super(KSJSB, self).openApp(Activity.HomeActivity)

    def reopenApp(self):
        self.freeMemory()
        self.openApp()

    def shouldReopen(self):
        pass

    def pressBackKey(self):
        currentFocus = self.adbIns.getCurrentFocus()
        activities = [
            Activity.PhotoDetailActivity,
            Activity.MiniAppActivity0,
            Activity.TopicDetailActivity,
            Activity.UserProfileActivity,
            Activity.AdYodaActivity
        ]
        for a in activities:
            if a in currentFocus:
                self.adbIns.pressBackKey()
                break
        if self.uIAIns.getDict(ResourceID.tab_text):
            self.adbIns.pressBackKey()
        elif self.uIAIns.getDict(ResourceID.comment_header_close, xml=self.uIAIns.xml):
            self.adbIns.pressBackKey()
        self.uIAIns.click(ResourceID.live_exit_button, xml=self.uIAIns.xml)
        self.uIAIns.click(ResourceID.exit_btn, xml=self.uIAIns.xml)
        self.uIAIns.click(ResourceID.button2, xml=self.uIAIns.xml)

    def initSleepTime(self):
        print('restTime=%s' % self.restTime)
        if self.restTime <= 0:
            return
        elif self.uIAIns.getDict(ResourceID.live_simple_play_swipe_text, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(ResourceID.open_long_atlas, xml=self.uIAIns.xml):
            pass
        elif self.uIAIns.getDict(ResourceID.choose_tv, xml=self.uIAIns.xml):
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
    def mainloop(cls, devicesSN):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            for i in cls.instances:
                i.watchVideo()
            print('现在是', datetime.now(), '，已运行：', datetime.now() - cls.startTime, sep='')
            sleep(1)
