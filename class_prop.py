class Foo():
    _myprop = 3

    @property
    def myprop(self):
        return self.__class__._myprop
    
    @myprop.setter
    def myprop(self, val):
        self.__class__._myprop = val

f = Foo()
g = Foo()

print(f.myprop, g.myprop)

f.myprop = 4

print(f.myprop, g.myprop)
