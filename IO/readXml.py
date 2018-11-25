# _*_ coding:UTF-8 _*_

from xml.etree.ElementTree import *


def readByElementTree(file):
    root = parse(file)
    student1 = root.findall("movie")
    for s in student1:
        print(s.find("type").text)



def main():
    readByElementTree("../data/xmlTest.xml")


if __name__ == '__main__':
    main()
