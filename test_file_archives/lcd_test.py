import unittest
from lcd import lcd_visuals as lv


test = lv()
myinput = ""
test.set_input("testing", myinput)
while myinput != "stop":
    test.output()
    myinput = input("test")
    test.set_input("testing", myinput)
