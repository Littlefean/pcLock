# PcLock 带监控的电脑锁

---

## 功能介绍

在鼠标和键盘没有操作之后的一段时间锁住电脑，进入第一阶段：锁定阶段

进入第一阶段后若继续持续一定时间没有操作，进入第二阶段：伪装蓝屏阶段

```
正常使用阶段  ==锁定==>  锁定阶段  ==屏幕出现蓝屏==> 伪装蓝屏阶段

```

在锁定阶段，鼠标吸附在中央无法移动。

在伪装蓝屏阶段，保留了鼠标无法移动的效果，同时还全屏蓝屏了。

在正常使用阶段，只要一移动鼠标或者键盘，就会使计时器清零。

如果计时器达到锁定标准，会锁定。进入第二阶段的计时器开启。

如果在锁定阶段移动鼠标，会让进入第二阶段的计时器清零。

**如果在伪装蓝屏的阶段移动了鼠标，会开启偷拍，把动你电脑的人偷拍下来，并将图片命名为时间保存到你的电脑里**

## 使用条件

windows操作系统，在安装了python的电脑上使用，开发环境 >= 3.7

使用软件 vieas 作为你的图片默认打开方式。

第三方库：

1. pyautogui
2. PIL
3. cv2
4. pynput

## 为什么不用windows自带的锁屏

我是一个mc服务器腐竹，在开服务器的时候如果锁屏了，服务器就断了，其他人就玩不了了。所以习惯了经常不锁屏。

后来有一天，有一个人在早晨趁我睡觉的时候坐在了我的座位上，顺便翻看了我的电脑，我醒来后那个人还坐在那里。这里点点那里点点。比较恐怖的是我不知道那个人看到了什么。



