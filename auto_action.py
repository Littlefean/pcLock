import time
import os
import random
import threading

import pyautogui
from PIL import Image, ImageGrab
import cv2


class Captor:
    """捕获者，包涵了截屏和拍照两种功能，用于捕捉“犯罪”证据"""

    def __init__(self, photo_path: str, screen_path: str):
        """

        :param photo_path:  照片保存路径：相对路径
        :param screen_path: 截屏保存路径：绝对路径
        """
        self.photo_path = photo_path
        self.screen_path = screen_path
        self.cap = cv2.VideoCapture(0)  # 开启摄像头对象
        ...

    def cap_screen(self):
        """截图并保存下来"""
        print("保存了截图")
        screenImg = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
        screenImg.save(f"{self.screen_path}/{self.file_name()}.png")

    def cap_camera(self):
        """
        捕捉摄像头并保存下来，目前发现摄像头保存的路径只能是相对路径
        :return:
        """
        ret, frame = self.cap.read()
        print(f"保存了图{self.file_name()}")
        cv2.imwrite(f'{self.photo_path}/{self.file_name()}.jpg', frame)  # 这个只能传入相对路径

    @staticmethod
    def file_name():
        return time.strftime("%Y-%m-%d week%w %H[%I]-%M-%S", time.localtime())

    # def startCamera(self, c: cv2.VideoCapture):
    #     """开启摄像头刷新，此线程会被阻塞，需要多线程开启"""
    #
    #     while True:
    #         # 开启条件是已经到了第二个锁阶段
    #         # 如果鼠标发生了移动
    #         p1 = pyautogui.position()
    #         time.sleep(0.1)
    #         p2 = pyautogui.position()
    #         if p1 != p2:
    #             saveImg(c, time.strftime("%Y-%m-%d week%w %H[%I]-%M-%S", time.localtime()))
    #         time.sleep(1)


class MouseAction:
    SCREEN_WIDTH = pyautogui.size().width
    SCREEN_HEIGHT = pyautogui.size().height

    def __init__(self):
        self.is_lock = False
        threading.Thread(target=self._interval).start()

    def _interval(self):
        while True:
            if self.is_lock:
                pyautogui.moveTo(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
            time.sleep(0.1)

    def lock(self):
        """执行此方法后会让鼠标吸附在屏幕中央"""
        self.is_lock = True
        ...

    def unlock(self):
        """执行此方法后悔解锁鼠标吸附中央的方法"""
        self.is_lock = False


def show_blue_screen():
    """
    展示蓝屏
    由于此方法会被阻塞，所以需要以多线程的方式开启此方法
    还需要基于安装软件 Vieas.exe 一个轻量级的图片查看软件，
    并将png图片或者jpg图片设置为系统默认打开方式
    注意：blueImg文件夹里只能放图片，不能放别的东西
    """

    def f():
        def enter():
            time.sleep(1.5)
            pyautogui.hotkey("enter")

        im = Image.open(f"blueImg\\{random.choice(os.listdir('blueImg'))}")
        threading.Thread(target=enter).start()
        im.show()

    threading.Thread(target=f).start()


def show_desktop():
    """桌面图标显示与隐藏的操作
    如果此方法执行两次，相当于没执行，抵消了"""
    pyautogui.hotkey("win", "d")
    pyautogui.moveTo(1, 1)
    pyautogui.rightClick()
    pyautogui.hotkey("v")
    pyautogui.hotkey("d")
