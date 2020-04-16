# --coding:utf-8--

def print_two(*args):
    arg1, arg2 = args
    print("arg1: %r, arg2: %r" % (arg1, arg2))


def print_two_agin(arg1, arg2):
    print("arg1: %r,arg2: %r" % (arg1, arg2))


def print_one(arg1):
    print("arg1: %r" % arg1)


def print_none():
    print("I got nothing.")


print_two("mik", "sala")
print_two_agin("mok", "salo")
print_one("First")
print_none()
