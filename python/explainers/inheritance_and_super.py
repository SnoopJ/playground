class Base:
    def __init__(self, data):
        print(f"Using Base.__init__() to create an instance of {self.__class__.__name__}, data={data}")
        self.data = data

    def calculate(self):
        # we have no calculation to do, just return the data
        # we expect that subclasses will override this method
        print("Calling Base.calculate()!")
        return self.data

class Adder(Base):
    # we don't need to write an __init__, we'll use the one from Base
    def calculate(self):
        print("Calling Adder.calculate()!")
        return self.data + 1

class Multiplier(Base):
    # we don't need to write an __init__
    def calculate(self):
        print("Calling Multiplier.calculate()!")
        return self.data * 2

class AddAgain(Adder):
    # we don't need to write an __init__, we'll use the one from Base
    def calculate(self):
        # here, we want to do whatever Adder did, *then* add another 2, so we call
        # the method on the parent class first
        print("Calling AddAgain.calculate()!")
        subtotal = super().calculate()  # super().calculate() will call Adder.calculate()
        return subtotal + 2  # then we add to the result of *that*


if __name__ == "__main__":
    a = Adder(42)
    aa = AddAgain(42)
    m = Multiplier(42)

    print(f"a.calculate = {a.calculate()}")
    print(f"m.calculate = {m.calculate()}")
    print(f"aa.calculate = {aa.calculate()}")
