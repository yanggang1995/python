# --coding:utf-8--
def cheese_and_crackers(cheese_count, boxes_of_crackers):
    print("You have %d cheeses!" % cheese_count)
    print("You have %d boxes of crackers!" % boxes_of_crackers)
    print("Main that's enough for a party!")
    print("Get a blanket.\n")


print("We can just give the function numbers directly:")
cheese_and_crackers(20, 30)

print("OR, we can use variables from our scrip:")
amount_of_cheese = 10
amount_of_crackers = 50
cheese_and_crackers(amount_of_cheese, amount_of_crackers)

print("We can even do math inside too:")
# 调用函数，传入数值运算的结果
cheese_and_crackers(10 + 20, 5 + 6)
# 打印语句
print("And we can combine the two, variables and math:")
# 调用函数，并且传递上面定义的参数运算后的值
cheese_and_crackers(amount_of_cheese + 100, amount_of_crackers + 1000)
