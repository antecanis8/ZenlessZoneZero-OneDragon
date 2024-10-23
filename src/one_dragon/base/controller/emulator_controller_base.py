import cv2

from cv2.typing import MatLike

from one_dragon.module.alas import AzurLaneAutoScript
from one_dragon.base.controller.controller_base import ControllerBase
from one_dragon.base.geometry.point import Point
class EmulatorControllerBase(ControllerBase):

    def __init__(self, win_title: str,
                 standard_width: int = 1920,
                 standard_height: int = 1080):
        ControllerBase.__init__(self)
        self.standard_width: int = standard_width
        self.standard_height: int = standard_height
        self.alas :AzurLaneAutoScript = AzurLaneAutoScript()

        self.sct = None

    def get_screenshot(self, independent: bool = False) -> MatLike:
        """
        截图 如果分辨率和默认不一样则进行缩放
        :return: 截图
        """
        screenshot = cv2.cvtColor(self.alas.device.screenshot(), cv2.COLOR_BGRA2RGB)
        cv2.imwrite('D:/Code_Work/antec/ZenlessZoneZero-OneDragon/888.png', screenshot)

        width = screenshot.shape[1]
        height = screenshot.shape[0]

        if width != self.standard_width and height != self.standard_height:
            result = cv2.resize(screenshot, (self.standard_width, self.standard_height),interpolation=cv2.INTER_AREA)
        else:
            result = screenshot
        return result

    def click(self, pos: Point = None, press_time: float = 0, pc_alt: bool = False) -> bool:
        """
        点击位置
        :param pos: 游戏中的位置 (x,y)
        :param press_time: 大于0时长按若干秒
        :param pc_alt: 只在PC端有用 使用ALT键进行点击
        :return: 不在窗口区域时不点击 返回False
        """
        pos.x=7.0/10*pos.x
        pos.y=2.0/3*pos.y
        if press_time is not None and press_time > 0:
            self.alas.device.long_clickxy(pos, press_time)
        else:
            self.alas.device.clickxy(pos)
        return True

    def drag_to(self, end: Point, start: Point = None, duration: float = 0.5):
        """
        按住拖拽
        :param end: 拖拽目的点
        :param start: 拖拽开始点
        :param duration: 拖拽持续时间
        :return:
        """
        from_pos: Point
        end.x=7.0/10*end.x
        end.y=2.0/3*end.y
        start.x=7.0/10*start.x
        start.y=2.0/3*start.y
        self.alas.device.drag(start, end, swipe_duration= duration,point_random=(0, 0, 0, 0),shake_random=(0, 0, 0, 0))

    def active_window(self) -> None:
        """
        前置窗口
        """
        self.alas.device.emulator_start()



