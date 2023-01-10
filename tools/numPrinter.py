# -*- encoding: utf-8 -*-
"""
大数字打印
2021年07月22日
by littlefean
"""
SOLID = "█"
SWALLOW = "  "
"""
  1
4   2
  3
7   5
  6
"""
numsBarDic = {
    1: [2, 5],
    2: [1, 2, 3, 7, 6],
    3: [1, 2, 3, 5, 6],
    4: [4, 3, 2, 5],
    5: [1, 4, 3, 5, 6],
    6: [1, 3, 4, 5, 6, 7],
    7: [1, 2, 5],
    8: [1, 2, 3, 4, 5, 6, 7],
    9: [1, 2, 3, 4, 5, 6],
    0: [1, 2, 4, 5, 6, 7],
}


def strN(n: int) -> str:
    """将数字转化成大型字符串"""
    marginRight = 2  # 数字与数字之间的页边距距离
    paddingLeft = 20  # 整个数字与左边框的距离
    paddingTop = 5  # 整个数字与顶部边框的距离
    numBarLen = 7  # 一个数字笔画杠杠的长度格子数量
    nStr = str(n)
    nums = len(nStr)
    arr = []
    arrW = nums * (numBarLen + marginRight)
    arrH = numBarLen * 2 - 1

    # 构建二维数组
    for y in range(arrH):
        line = []
        for x in range(arrW):
            line.append(SWALLOW)
        arr.append(line)

    # 从左到右遍历每一个数字
    for i in range(nums):
        n = eval(nStr[i])
        barCodeArr = numsBarDic[n]
        leftX = i * (numBarLen + marginRight)
        for barCode in barCodeArr:
            if barCode == 1:
                for x in range(leftX, leftX + numBarLen):
                    arr[0][x] = SOLID
            if barCode == 2:
                for y in range(numBarLen):
                    arr[y][leftX + numBarLen - 1] = SOLID
            if barCode == 3:
                for x in range(leftX, leftX + numBarLen):
                    arr[numBarLen - 1][x] = SOLID
            if barCode == 4:
                for y in range(numBarLen):
                    arr[y][leftX] = SOLID
            if barCode == 5:
                for y in range(numBarLen):
                    arr[numBarLen - 1 + y][leftX + numBarLen - 1] = SOLID
            if barCode == 6:
                for x in range(leftX, leftX + numBarLen):
                    arr[arrH - 1][x] = SOLID
            if barCode == 7:
                for y in range(numBarLen):
                    arr[numBarLen - 1 + y][leftX] = SOLID

    for y in range(len(arr)):
        arr[y] = [SWALLOW] * paddingLeft + arr[y]
    for i in range(paddingTop):
        arr = [[SWALLOW] * len(arr[-1])] + arr

    res = ""
    for y in range(len(arr)):
        for x in range(len(arr[0])):
            res += arr[y][x]
        res += "\n"
    return res


if __name__ == '__main__':

    print(strN(890))
    input("end...")
