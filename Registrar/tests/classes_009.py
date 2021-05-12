class Test  ():
    def function (self, some_param = None):
        print(some_param)

if __name__ == "__main__":
    t = Test()
    t.function("hello")
    t.function(some_param = "hello")
    # t.function(some_param = "hello", some_other_param = "hello") # errors out
