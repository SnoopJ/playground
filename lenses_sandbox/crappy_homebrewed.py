"""
  mcspud introduced me to the idea of Lenses ("functional references") for
  manipulating highly structured data, so this is all his fault

  none of this works really at all, it's just for fun
"""
from compose import compose
from copy import deepcopy

class LensError(ValueError):
    pass

class Lens():
    def __init__(self, prop):
        self._prop = prop

    def __call__(self, data):
        """ bind? """
        try:
            return data[self._prop]
        except KeyError:
            return getattr(data, str(self._prop))
        else:
            raise LensError

    def get(self):
        pass

    def __mul__(self, other):
        """
        Multiplication L1*L2 applies lenses as L2(L1(...)), so that reading a
        string of lenses from left-to-right corresponds to outer-to-inner in a
        data structure.
        """
        return compose(other, self)

    def __getattr__(self, attr):
        """ Truly evil hack to allow `lens1 . lens2` a la Haskell. Mostly frippery. """
        return globals()[str(attr)] * self


if __name__ == '__main__':
    data = {'foo': 
            { 'bar': [
                {1: 'taco', 2: 'butt'},
                {1: 'cat', 2: 'sauce'}
                ]
            } 
           }

    foo = Lens('foo')
    bar = Lens('bar')
    l1 = Lens(1)
    l2 = Lens(2)

    print((foo*bar)(data))
