import threading
import time


class StageClock:
    """
    阶段表 单例模式
    假如 t1 = 3   t2 = 7
    秒表开始走
    0 1 2 3 4 5 6 7 8 9 10

    走到 3触发一次函数1
    走到 7触发一次函数2

    """

    def __init__(self, t1: int, t2: int):
        """

        :param t1: 第一阶段时间
        :param t2: 第二阶段时间
        """
        self.lock_time_1 = t1
        self.lock_time_2 = t2
        self._t = 0  # 记录已经多少秒没有动弹了

        self.status1_target = lambda: ...  # 第一阶段到达所触发的动作
        self.status2_target = lambda: ...  # 第二阶段到达所触发的动作
        ...

    def get_stage(self):
        """0表示没有锁住 1表示只锁了鼠标 2表示伪装阶段"""
        if self._t < self.lock_time_1:
            return 0
        if self._t < self.lock_time_2:
            return 1
        return 2

    def start(self):
        """阶段锁开始运行，计时开始"""
        threading.Thread(target=self._go_tick).start()

    def reset(self):
        """向前拨回时间"""
        if self._t <= self.lock_time_1:
            self._t = 0
        elif self._t <= self.lock_time_2:
            self._t = self.lock_time_1 + 1
        else:
            self._t = self.lock_time_2 + 1

    def clear(self):
        """向前拨回到0"""
        self._t = 0

    def _go_tick(self):
        while True:
            time.sleep(1)
            self._t += 1
            print(self._t)
            if self._t == self.lock_time_1:
                self.status1_target()
            if self._t == self.lock_time_2:
                self.status2_target()

    ...
