#include <stdio.h>
#include <windows.h>
#include <conio.h>
#include <process.h>

const int FREEZE_FREQUENCY = 50; // 锁定鼠标频率 毫秒
const int UPDATE_FREQUENCY = 300; // 鼠标检测频率 毫秒

int SECOND = 0; // 全局变量
int STATUS = 0; // 是否锁住了
int ANSWER = 0; // 是否回答对了

POINT MOUSE_LOC = {0, 0};

/**
 * 更新鼠标位置变量
 */
_Noreturn void UpDateMouse(void) {
    while (1) {
        GetCursorPos(&MOUSE_LOC);
        Sleep(UPDATE_FREQUENCY);
    }
}

/**
 * 键盘监听解锁鼠标的线程函数
 */
void HearAnswer() {
    printf("new process running\n");
    int ch;
    //循环监听
    while (1) {
        printf("\tplease input...");
        ch = getch();

        // 直到按 Esc键 或者 Tab键 退出
        if (ch == 27 || ch == 9) {
            ANSWER = 1;
            printf("RIGHT~\a\n");
            break;
        } else {
            printf("your input value is wrong: %d\n", ch);
        }
    }
    _endthread();
}

/**
 * 在终端打印出一些红颜色的醒目的东西
 */
void printRed() {
    HANDLE hConsole;
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, BACKGROUND_RED);
    for (int y = 0; y < 20; y++) {
        for (int x = 0; x < 100; x++) {
            printf(" ");
        }
        printf("\n");
    }
}

/**
 * 发出提示音，多线程函数
 */
void alarm() {
    for (int i = 0; i < 2; i++) {
        Beep(250 - i * 20, 150);
        Sleep(50);
    }
    _endthread();
}


int main() {
    // 开启鼠标实时更新线程
    _beginthread((void (*)(void *)) UpDateMouse, 0, NULL);

    POINT SAVE_LOC = {0, 0};  // 保存的鼠标位置

    GetCursorPos(&SAVE_LOC);

    while (1) {

        Sleep(1000);
        // 移动检测
        if (!(SAVE_LOC.x == MOUSE_LOC.x && SAVE_LOC.y == MOUSE_LOC.y)) {
            // 如果动了，计时器清零
            SECOND = 0;
        }
        // 锁定检测
        if (SECOND >= 30) {
            // 在这里就要把它锁住了。
            SECOND = 0;
            STATUS = 1;
            // 开启键盘监听线程
            _beginthread((void (*)(void *)) HearAnswer, 0, NULL);
            // 开启播放提示音线程
            _beginthread((void (*)(void *)) alarm, 0, NULL);
            // 打印红字以醒目
            printRed();
            while (1) {
                if (ANSWER) {
                    STATUS = 0;
                    ANSWER = 0;
                    break;
                }
                SetCursorPos(GetSystemMetrics(SM_CXSCREEN) / 2, GetSystemMetrics(SM_CYSCREEN) / 2);
                Sleep(FREEZE_FREQUENCY);
            }
        }
        if (STATUS) {
            printf("locked!\n");
            continue;
        } else {
            SECOND++;
            GetCursorPos(&SAVE_LOC);
            printf("second count: %d\n", SECOND);
        }
        // 消掉ide的警告
        if (SECOND == 2147483647) {
            break;
        }
    }
    return 0;
}
