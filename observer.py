"""
检测者
"""

import threading

from pynput import mouse


class Observer:
    """观察者  封装了鼠标"""

    def __init__(self):
        self.mouse_move_target = None
        self.mouse_click_target = None
        self.mouse_scroll_target = None
        self.mouse_middle_target = None
        ...

    def start(self):
        def on_move(x, y):
            # 监听鼠标移动
            self.mouse_move_target()

        def on_click(x, y, button, pressed):
            self.mouse_click_target()
            if button == mouse.Button.middle and pressed:
                print("鼠标点击了中键！！")
                self.mouse_middle_target()

        def on_scroll(x, y, dx, dy):
            self.mouse_scroll_target()

        def mouse_add_hock():
            """由于以下代码会造成阻塞，所以需要用多线程来开启此函数"""
            with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
                listener.join()

        # 添加鼠标事件刷新
        threading.Thread(target=mouse_add_hock).start()
        ...

    ...
