# _*_ coding:UTF-8 _*_

# 最简单、最快速处理文本文件的做法，for循环文件对象取出每一行数据
import os

# for line in open("D:\STARCOR\MISSION\内蒙频道id一对多\盟市\阿拉善新闻综合.txt", "rb"):
#     print(bytes.decode(line).rstrip("\n"))  # 取出的一行数据末尾会有\n
from datetime import time

pathDir = os.listdir("D:\STARCOR\MISSION\内蒙频道id一对多\盟市")
for allDir in pathDir:
    print(allDir)
    child = os.path.join('%s\\%s' % ("D:\STARCOR\MISSION\内蒙频道id一对多\盟市", allDir))
    print(child)

    for line in open(child, "rb"):
        try:
            # 取出的一行数据末尾会有\n
            str = line.decode("utf-8").rstrip("\n")
        except Exception:
            str = line.decode("gb2312").rstrip("\n")
        print(str)

