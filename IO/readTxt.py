# _*_ coding:UTF-8 _*_

# 最简单、最快速处理文本文件的做法，for循环文件对象取出每一行数据
for line in open("../data/test01.txt", "r+"):
    print(line.rstrip('\n'))  # 取出的一行数据末尾会有\n
