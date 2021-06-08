class Test ():
    def __init__ (self, name):
        self.name = name

if __name__ == "__main__":
    t1 = Test("Test_1")
    t2 = Test("Test_2")
    t3 = Test("Test_3")
    objects = [ t1, t2, t3 ]
    print(objects)
    objects.remove(Test(name = t1.name))