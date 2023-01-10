from stage_clock import StageClock
from observer import Observer
from auto_action import Captor, MouseAction, show_blue_screen


def main():
    mouse = MouseAction()
    cap = Captor("result", "D:/桌面/grabRes")

    clock = StageClock(10, 20)

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


if __name__ == "__main__":
    main()
