from .project import Project
from ..tools import sleep


class ResourceID:
    icon_title = 'com.miui.home:id/icon_title'  # 桌面图标


class IQ(Project):
    def __init__(self):
        super(IQ, self).__init__('201')

    def mainloop(self):
        while True:
            if self.adbIns.rebootPerHour():
                self.uIAIns.click(ResourceID.icon_title, '新自阅')
            sleep(1200)
