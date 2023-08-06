from .project import Project


class ResourceID:
    button2 = 'android:id/button2'  # 确定（联机业务异常，请重新联机）、立即连接（连接异常,正在重新连接......）


class SD(Project):
    instances = []

    def __init__(self, SN):
        super(SD, self).__init__(SN)

    def check(self):
        try:
            self.uIAIns.click(ResourceID.button2)
        except FileNotFoundError as e:
            print(e)
            self.check()

    @classmethod
    def mainloop(cls, devicesSN):
        for deviceSN in devicesSN:
            cls.instances.append(cls(deviceSN))
        while True:
            for i in cls.instances:
                i.check()
