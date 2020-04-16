# --coding:utf-8--
from sys import argv

script, filename = argv
txt = open(filename, encoding=ascii("utf-8"))
print("Here's your file %r:" % filename)
print(txt.read())
print("Type the filename again:", end="")
file_again = input(">")
print(open(file_again).read())
