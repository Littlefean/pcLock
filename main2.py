from stageClock import StageClock
from observer import Observer
from autoAction import Captor, MouseAction, showBlue

from time import sleep


def main():
    mouse = MouseAction()
    cap = Captor("...", "...")

    clock = StageClock()

    clock.status1_target = mouse.lock
    clock.status2_target = showBlue

    obs = Observer()

    def move():
        # 别人在动电脑的时候触发这个函数
        if clock.get_stage() == 1:
            clock.reset()
        elif clock.get_stage() == 2:
            clock.reset()
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

    sleep(100000)
    ...


if __name__ == "__main__":
    main()