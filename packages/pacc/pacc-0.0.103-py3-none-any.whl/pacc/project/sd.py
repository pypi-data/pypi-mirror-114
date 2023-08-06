from .project import Project
from ..tools import sleep


class ResourceID:
    button2 = 'android:id/button2'  # 确定（联机业务异常，请重新联机）、立即连接（连接异常,正在重新连接......）
    mec_connect_state = 'com.dd.rclient:id/mec_connect_state'  # 正在连接服务器...
    btn_exit_app = 'com.dd.rclient:id/btn_exit_app'  # 退出程序
    icon_title = 'com.miui.home:id/icon_title'  # 桌面图标


class SD(Project):
    instances = []

    def __init__(self, SN):
        super(SD, self).__init__(SN)

    def check(self):
        try:
            self.uIAIns.click(ResourceID.button2)
            dic = self.uIAIns.getDict(ResourceID.mec_connect_state, xml=self.uIAIns.xml)
            if dic and dic['@text'] == '正在连接服务器...':
                self.reopenApp()
        except FileNotFoundError as e:
            print(e)
            self.check()

    def reopenApp(self):
        self.exitApp()
        self.openApp()

    def openApp(self):
        self.uIAIns.click(ResourceID.icon_title, '滴滴助手')
        sleep(9)
        self.uIAIns.click('com.dd.rclient:id/auto_wait_btn')

    def exitApp(self):
        self.uIAIns.click(ResourceID.btn_exit_app, xml=self.uIAIns.xml)
        self.uIAIns.click(ResourceID.button2)

    @classmethod
    def mainloop(cls, devicesSN):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            for i in cls.instances:
                i.check()
            sleep(600)
