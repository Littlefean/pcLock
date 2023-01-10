"""
致力于不锁屏的状态下自动锁电脑
该程序只进行简单的锁机制

todo 还能让手机控制电脑锁屏
2021.2.14
by littlefean
"""
import os
import random
import time
import threading

import pyautogui
import keyboard
from PIL import Image
from PIL import ImageGrab
from pynput import mouse
import cv2

pyautogui.FAILSAFE = False

LOCK_SECOND_1 = 60  # 到达第一阶段锁的秒数
LOCK_SECOND_2 = 600  # 到达第二阶段锁的秒数

SCREEN_WIDTH = pyautogui.size().width
SCREEN_HEIGHT = pyautogui.size().height

SLOW_FREQUENCY = 1
FAST_FREQUENCY = 0.0000001
freezeFrequency = SLOW_FREQUENCY

"""
达到第一锁定阶段：
鼠标一直被吸附在屏幕中央
达到第二锁定阶段：
显示假装电脑蓝屏的图片 全屏显示
"""
isLocked1 = False  # 表示现在的状态是不是锁住了
isLocked2 = False  # 表示现在是不是已经经过了第二道锁

answer = False  # 是否回答正确
second = 0  # 记录已经有多少秒没动了


def main():
    global second, isLocked1, answer, isLocked2, freezeFrequency
    cap = cv2.VideoCapture(0)  # 开启摄像头对象

    print("开始准备")
    # 添加键盘刷新
    threading.Thread(target=keyboardAddHock).start()
    # 添加鼠标事件刷新
    threading.Thread(target=mouseAddHock).start()
    print("准备完毕")
    # 开启等待秒数更新
    threading.Thread(target=timeGo).start()
    # 鼠标锁开启
    threading.Thread(target=lock1).start()
    # 摄像头刷新开启
    threading.Thread(target=startCamera, args=(cap,)).start()
    while True:
        # 开启消息事件循环
        if second >= LOCK_SECOND_1:
            # 如果秒数超过了第一阶段时间
            isLocked1 = True
            freezeFrequency = FAST_FREQUENCY
        if second == LOCK_SECOND_2:
            # 如果秒数到了第二阶段时间
            lock2()
        if answer:
            # 如果解锁正确
            isLocked1 = False
            freezeFrequency = SLOW_FREQUENCY
            answer = False
            isLocked2 = False
            second = 0
        time.sleep(0.2)


def startCamera(c: cv2.VideoCapture):
    """开启摄像头刷新，此线程会被阻塞，需要多线程开启"""

    while True:
        if isLocked2:
            # 开启条件是已经到了第二个锁阶段
            # 如果鼠标发生了移动
            p1 = pyautogui.position()
            time.sleep(0.1)
            p2 = pyautogui.position()
            if p1 != p2:
                saveImg(c, time.strftime("%Y-%m-%d week%w %H[%I]-%M-%S", time.localtime()))
        time.sleep(1)


def saveImg(c: cv2.VideoCapture, fileName: str):
    """让摄像头拍一张照片并保存下来，同时截图对应的屏幕保存下来"""
    ret, frame = c.read()
    print(f"保存了图{fileName}")
    screenImg = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
    cv2.imwrite(f'result\\{fileName}.jpg', frame)  # 这个只能传入相对路径
    screenImg.save(f"D:\\桌面\\grabRes\\{fileName}.png")


def lock2():
    """开始第二道锁"""
    global isLocked2
    if not isLocked2:
        print("开始出现蓝屏了")
        threading.Thread(target=showBlue).start()
        isLocked2 = True


def lock1():
    """开启第一道锁
    由于该线程会阻塞，所以需要多线程的方式开启"""
    # global FREEZE_FREQUENCY
    while True:
        if isLocked1:
            pyautogui.moveTo(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        time.sleep(freezeFrequency)


def showBlue():
    """
    展示蓝屏
    由于此方法会被阻塞，所以需要以多线程的方式开启此方法
    还需要基于安装软件 Vieas.exe 一个轻量级的图片查看软件，
    并将png图片或者jpg图片设置为系统默认打开方式
    注意：blueImg文件夹里只能放图片，不能放别的东西
    """

    def enter():
        time.sleep(1.5)
        pyautogui.hotkey("enter")

    im = Image.open(f"blueImg\\{random.choice(os.listdir('blueImg'))}")
    threading.Thread(target=enter).start()
    im.show()


def desktopAction():
    """桌面图标显示与隐藏的操作
    如果此方法执行两次，相当于没执行，抵消了"""
    pyautogui.hotkey("win", "d")
    pyautogui.moveTo(1, 1)
    pyautogui.rightClick()
    pyautogui.hotkey("v")
    pyautogui.hotkey("d")


def hideDesktop():
    """快速显示到桌面并隐藏图标"""
    global isLocked2
    if not isLocked2:
        desktopAction()
        isLocked2 = True


def timeGo():
    global second
    while True:
        second += 1
        print(second)
        time.sleep(1)


def resetByKeyboard(e):
    resetSecond()
    print(e, e.scan_code)


def keyboardAddHock():
    keyboard.hook(resetByKeyboard)
    print("ready")


def mouseAddHock():
    """由于以下代码会造成阻塞，所以需要用多线程来开启此函数"""
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()


def resetSecond():
    """重置锁倒计时，一般用于某个事件发生而重新计时"""
    global second
    if not isLocked1:
        second = 0
    if isLocked1 and not isLocked2:
        second = LOCK_SECOND_1


def unlock():
    """解锁，修改数据"""
    global answer, isLocked1
    print(f"正在解锁 当前锁状态: {isLocked1}, 是否回答正确: {answer}")
    if isLocked1:
        answer = True
        print("解锁成功!")
    else:
        print("不是解锁的时候")


def keyBoardAnswer():
    """
    键盘监听解锁鼠标线程函数
    :return:
    """
    keyboard.add_hotkey("tab", unlock)


def on_move(x, y):
    # 监听鼠标移动
    resetSecond()
    # print('Pointer moved to {0}'.format((x, y)))


def on_click(x, y, button, pressed):
    resetSecond()
    if button == mouse.Button.middle and pressed:
        unlock()
    # print("pressed", x, y, button, pressed)


def on_scroll(x, y, dx, dy):
    resetSecond()
    # print("scroll")


if __name__ == '__main__':
    main()
