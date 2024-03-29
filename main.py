from tkinter import *
from stage_clock import StageClock
from observer import Observer
from auto_action import Captor, MouseAction, show_blue_screen


def main():
    mouse = MouseAction()
    cap = Captor("result", "D:/桌面/grabRes")

    clock = StageClock(60, 600)

    clock.status1_target = mouse.lock
    clock.status2_target = show_blue_screen

    obs = Observer()

    def move():
        # 别人在动电脑的时候触发这个函数
        clock.reset()
        if clock.get_stage() == 2:
            cap.cap_camera()
            cap.cap_screen()

    def unlock():
        # 在解锁的时候触发
        clock.clear()
        mouse.unlock()

    obs.mouse_move_target = move
    obs.mouse_click_target = move
    obs.mouse_scroll_target = move

    obs.mouse_middle_target = unlock
    obs.start()

    clock.start()

    root = Tk()
    root.title("hello world")
    root.geometry('250x100')  # 是x 不是*
    root.resizable(width=False, height=True)  # 宽不可变, 高可变,默认为True
    root.mainloop()


if __name__ == "__main__":
    main()
