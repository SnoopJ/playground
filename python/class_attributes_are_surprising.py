"""
Based on a requested code review in freenode #python. The original sample
used class attributes like WrongCar, this is an example of why that's usually
not what a user wants
"""

print("...doing things the wrong way...")


class WrongCar:
    """ This class shows why CLASS ATTRIBUTES (below) are generally WRONG """

    model = "Nissan"
    mpg = 30

    def __init__(self):
        pass


nissan = WrongCar()
print("Before modification\n---")
print(f"{nissan.model = }")
print()

# I want a SEPARATE car that's a Honda, now,
# and the only way to do it is...
WrongCar.model = "Honda"
honda = WrongCar()

print("After modification\n---")
print(f"{honda.model = }")
print(f"{nissan.model = } (uh oh!)")
print()

# model is a CLASS ATTRIBUTE, so it will change on every instance if
# it ever changes. This doesn't make sense! Every car object has its
# own properties, and if we want to change them, it should only change
# that one object!

print("...doing things the right way...\n")


class RightCar:
    """ This class sets model and mpg as INSTANCE ATTRIBUTES """

    def __init__(self, model="Nissan", mpg=30):  # we can still have defaults
        self.model = model  # these are INSTANCE ATTRIBUTES, i.e. only on THIS object
        self.mpg = mpg


nissan = RightCar()
honda = RightCar(model="Honda")

print("Before modification\n---")
print(f"{nissan.model = }, {nissan.mpg = }")
print(f"{honda.model = }, {honda.mpg = }")

# oops, the fuel injectors in the Honda got dirty, so the mpg has to go down!

honda.mpg = 25

print("After modification\n---")
print(f"{nissan.model = }, {nissan.mpg = }")
print(f"{honda.model = }, {honda.mpg = }")

# notice that the mpg property of the nissan object did NOT change, because what
# we are changing is an INSTANCE ATTRIBUTE
